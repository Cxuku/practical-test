<?php
declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use App\Database;

if (file_exists(__DIR__ . '/../.env')) {
    $dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/..');
    $dotenv->load();
}

$customers = [];
$error     = null;

try {
    $db   = new Database();
    $pdo  = $db->getConnection();

    $stmt = $pdo->prepare(
        'SELECT id, name, email, created_at FROM customers ORDER BY created_at DESC'
    );
    $stmt->execute();
    $customers = $stmt->fetchAll(PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    $error = 'Unable to connect to the database. Please try again later.';
    error_log('[' . date('Y-m-d H:i:s') . '] DB Error: ' . $e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Records</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5;
            padding: 2rem;
            color: #1f2937;
        }
        .container { max-width: 960px; margin: 0 auto; }
        h1 { font-size: 1.8rem; color: #1a1a2e; margin-bottom: 0.4rem; }
        .subtitle { color: #6b7280; font-size: 0.9rem; margin-bottom: 1.5rem; }
        .error {
            background: #fee2e2; border: 1px solid #f87171; color: #dc2626;
            padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.25rem;
            font-size: 0.95rem;
        }
        .card {
            background: #fff; border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden;
        }
        table { width: 100%; border-collapse: collapse; }
        thead { background: #1a1a2e; color: #fff; }
        th {
            padding: 0.9rem 1.2rem; text-align: left;
            font-size: 0.78rem; font-weight: 600;
            text-transform: uppercase; letter-spacing: 0.06em;
        }
        td { padding: 0.85rem 1.2rem; border-bottom: 1px solid #f1f5f9; font-size: 0.92rem; }
        tr:last-child td { border-bottom: none; }
        tbody tr:hover td { background: #f8fafc; }
        .row-num {
            display: inline-block; background: #ede9fe; color: #6d28d9;
            padding: 2px 9px; border-radius: 99px; font-size: 0.75rem; font-weight: 700;
        }
        .empty { text-align: center; padding: 3rem; color: #9ca3af; font-size: 0.95rem; }
    </style>
</head>
<body>
<div class="container">
    <h1>Customer Records</h1>
    <p class="subtitle">Live data from the customers table</p>

    <?php if ($error !== null): ?>
        <div class="error"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></div>
    <?php else: ?>
        <p class="subtitle">Showing <?= count($customers) ?> record(s)</p>
        <div class="card">
            <?php if (empty($customers)): ?>
                <p class="empty">No customers found in the database.</p>
            <?php else: ?>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Created At</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($customers as $i => $customer): ?>
                            <tr>
                                <td><span class="row-num"><?= $i + 1 ?></span></td>
                                <td><?= htmlspecialchars((string)$customer['id'], ENT_QUOTES, 'UTF-8') ?></td>
                                <td><?= htmlspecialchars($customer['name'], ENT_QUOTES, 'UTF-8') ?></td>
                                <td><?= htmlspecialchars($customer['email'], ENT_QUOTES, 'UTF-8') ?></td>
                                <td><?= htmlspecialchars($customer['created_at'], ENT_QUOTES, 'UTF-8') ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        </div>
    <?php endif; ?>
</div>
</body>
</html>
