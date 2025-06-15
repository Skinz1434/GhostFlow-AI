-- GhostFlow AI database schema

-- Table for click tracking
CREATE TABLE IF NOT EXISTS clicks (
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    ip TEXT NOT NULL,
    ua TEXT NOT NULL,
    ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Table for key performance indicators
CREATE TABLE IF NOT EXISTS kpi (
    id SERIAL PRIMARY KEY,
    metric TEXT NOT NULL,
    val NUMERIC NOT NULL,
    ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Table for financial ledger entries
CREATE TABLE IF NOT EXISTS ledger (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
