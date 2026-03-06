const pool = require('../db');

// Create a new ticket
exports.createTicket = async (req, res) => {
    try {
        const { title, description, status, priority, assigned_to } = req.body;
        const result = await pool.query(
            'INSERT INTO ticket (title, description, status, priority, assigned_to) VALUES ($1, $2, COALESCE($3, \'open\'), COALESCE($4, \'medium\'), $5) RETURNING *',
            [title, description, status, priority, assigned_to || null]
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Get all tickets
exports.getTickets = async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM ticket ORDER BY id ASC');
        res.status(200).json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Get a single ticket by ID
exports.getTicketById = async (req, res) => {
    try {
        const { id } = req.params;
        const result = await pool.query('SELECT * FROM ticket WHERE id = $1', [id]);
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Ticket not found' });
        }
        res.status(200).json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Update a ticket
exports.updateTicket = async (req, res) => {
    try {
        const { id } = req.params;
        const { title, description, status, priority, assigned_to } = req.body;
        const result = await pool.query(
            `UPDATE ticket 
       SET title = COALESCE($1, title), 
           description = COALESCE($2, description), 
           status = COALESCE($3, status), 
           priority = COALESCE($4, priority), 
           assigned_to = $5,
           updated_at = NOW()
       WHERE id = $6 RETURNING *`,
            [title, description, status, priority, assigned_to, id]
        );
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Ticket not found' });
        }
        res.status(200).json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};

// Delete a ticket
exports.deleteTicket = async (req, res) => {
    try {
        const { id } = req.params;
        const result = await pool.query('DELETE FROM ticket WHERE id = $1 RETURNING *', [id]);
        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'Ticket not found' });
        }
        res.status(200).json({ message: 'Ticket deleted successfully' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
};
