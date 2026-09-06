-- ==============================================================================
-- SovereignAI — Production Database Schema & Seed Data (PostgreSQL 16)
-- Enterprise Agentic AI Workbench for Confidential Industrial Work
-- ==============================================================================

-- Clean previous tables if running fresh restore
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 2. Conversations Table
CREATE TABLE conversations (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user ON conversations(user_id);

-- 3. Messages Table
CREATE TABLE messages (
    id VARCHAR(255) PRIMARY KEY,
    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conv ON messages(conversation_id);

-- 4. Documents Table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(1024) NOT NULL,
    mime_type VARCHAR(100) DEFAULT 'application/pdf',
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'error'
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_status ON documents(status);

-- ==============================================================================
-- SEED DATA: Industrial Workstation Demo & Initial Superuser
-- ==============================================================================

-- 1. Default Admin & Engineer Users
INSERT INTO users (id, username, email, hashed_password, is_active, is_superuser) VALUES
(1, 'admin', 'admin@sovereign.local', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE, TRUE),
(2, 'engineer_pankaj', 'engineer@sovereign.local', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE, FALSE)
ON CONFLICT (id) DO NOTHING;

-- 2. Sample Industrial Conversation
INSERT INTO conversations (id, title, user_id) VALUES
('conv_turbopump_audit', 'Turbopump Valve Inspection & Safety Audit', 2)
ON CONFLICT (id) DO NOTHING;

-- 3. Messages in Conversation
INSERT INTO messages (id, conversation_id, role, content, metadata_json) VALUES
('msg_001', 'conv_turbopump_audit', 'user', 'Please review the inspection log for Valve B-12 and verify standard operating pressure.', '{"source": "web_chat"}'),
('msg_002', 'conv_turbopump_audit', 'assistant', 'According to Standard Operating Procedure SOP-774, Valve B-12 nominal operating pressure is 450 PSI (+/- 15 PSI). The latest inspection reading showed 448 PSI, which is well within normal safe operating thresholds.', '{"agent": "industrial_sop_agent", "confidence": 0.98}')
ON CONFLICT (id) DO NOTHING;

-- 4. Sample Document
INSERT INTO documents (id, filename, filepath, mime_type, status, user_id) VALUES
(1, 'Turbopump_Inspection_Report_2026.pdf', '/storage/uploads/dummy.pdf', 'application/pdf', 'completed', 2)
ON CONFLICT (id) DO NOTHING;
