function notFound(req, res, next) {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'API endpoint not found' });
  }
  next();
}

function errorHandler(err, req, res, next) {
  console.error('Error:', err.message);
  if (req.path.startsWith('/api/')) {
    return res.status(500).json({ error: 'Internal server error' });
  }
  next(err);
}

module.exports = { notFound, errorHandler };
