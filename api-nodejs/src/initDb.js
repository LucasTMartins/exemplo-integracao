const pool = require('./db');

const initDb = async () => {
    const createUserTable = `
    CREATE TABLE IF NOT EXISTS user_assign (
        id          SERIAL PRIMARY KEY,
        name        VARCHAR(100) NOT NULL,
        email       VARCHAR(150) NOT NULL UNIQUE,
        created_at  TIMESTAMP DEFAULT NOW()
    );
  `;

    const createTicketTable = `
    CREATE TABLE IF NOT EXISTS ticket (
        id            SERIAL PRIMARY KEY,
        title         VARCHAR(255) NOT NULL,
        description   TEXT,
        status        VARCHAR(50) NOT NULL DEFAULT 'open',
        priority      VARCHAR(20) NOT NULL DEFAULT 'medium',
        assigned_to   INT REFERENCES user_assign(id) ON DELETE SET NULL,
        created_at    TIMESTAMP DEFAULT NOW(),
        updated_at    TIMESTAMP DEFAULT NOW()
    );
  `;

    try {
        await pool.query(createUserTable);
        console.log('user_assign table verified/created.');
        await pool.query(createTicketTable);
        console.log('ticket table verified/created.');
    } catch (err) {
        console.error('Error initializing database:', err);
    } finally {
        pool.end();
    }
};

initDb();
