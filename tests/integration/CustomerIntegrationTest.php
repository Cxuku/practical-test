<?php
declare(strict_types=1);

namespace Tests\Integration;

use PDO;
use PHPUnit\Framework\TestCase;

class CustomerIntegrationTest extends TestCase
{
    private ?PDO $pdo = null;

    protected function setUp(): void
    {
        $host     = $_ENV['TEST_DB_HOST']     ?? getenv('TEST_DB_HOST')     ?: '127.0.0.1';
        $port     = $_ENV['TEST_DB_PORT']     ?? getenv('TEST_DB_PORT')     ?: '3306';
        $dbname   = $_ENV['TEST_DB_NAME']     ?? getenv('TEST_DB_NAME')     ?: 'test_db';
        $username = $_ENV['TEST_DB_USER']     ?? getenv('TEST_DB_USER')     ?: 'root';
        $password = $_ENV['TEST_DB_PASSWORD'] ?? getenv('TEST_DB_PASSWORD') ?: '';

        $dsn = "mysql:host={$host};port={$port};dbname={$dbname};charset=utf8mb4";

        $this->pdo = new PDO($dsn, $username, $password, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);

        $this->pdo->exec('
            CREATE TABLE IF NOT EXISTS customers (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                name       VARCHAR(100)  NOT NULL,
                email      VARCHAR(150)  NOT NULL UNIQUE,
                created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
            )
        ');
    }

    protected function tearDown(): void
    {
        $this->pdo?->exec('DROP TABLE IF EXISTS customers');
        $this->pdo = null;
    }

    public function testCanInsertAndFetchCustomer(): void
    {
        $stmt = $this->pdo->prepare(
            'INSERT INTO customers (name, email) VALUES (:name, :email)'
        );
        $stmt->execute([':name' => 'Jane Doe', ':email' => 'jane@example.com']);

        $stmt = $this->pdo->prepare(
            'SELECT id, name, email, created_at FROM customers WHERE email = :email'
        );
        $stmt->execute([':email' => 'jane@example.com']);
        $customer = $stmt->fetch();

        $this->assertIsArray($customer);
        $this->assertSame('Jane Doe', $customer['name']);
        $this->assertSame('jane@example.com', $customer['email']);
    }

    public function testFetchAllReturnsMultipleRows(): void
    {
        $stmt = $this->pdo->prepare(
            'INSERT INTO customers (name, email) VALUES (:name, :email)'
        );
        $stmt->execute([':name' => 'Alice', ':email' => 'alice@example.com']);
        $stmt->execute([':name' => 'Bob',   ':email' => 'bob@example.com']);

        $stmt = $this->pdo->prepare(
            'SELECT id, name, email, created_at FROM customers ORDER BY created_at DESC'
        );
        $stmt->execute();
        $rows = $stmt->fetchAll();

        $this->assertCount(2, $rows);
    }

    public function testPreparedStatementPreventsInjection(): void
    {
        $malicious = "'; DROP TABLE customers; --";

        $stmt = $this->pdo->prepare(
            'SELECT id FROM customers WHERE name = :name'
        );
        $stmt->execute([':name' => $malicious]);
        $result = $stmt->fetchAll();

        // Table still intact — prepared statement neutralised the injection
        $this->assertIsArray($result);

        $check = $this->pdo->query('SELECT COUNT(*) AS cnt FROM customers');
        $this->assertNotFalse($check);
    }
}
