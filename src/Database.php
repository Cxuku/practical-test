<?php
declare(strict_types=1);

class Database
{
    private ?PDO $connection = null;

    public function getConnection(): PDO
    {
        if ($this->connection !== null) {
            return $this->connection;
        }

        $host     = $_ENV['DB_HOST']     ?? getenv('DB_HOST')     ?: 'localhost';
        $port     = $_ENV['DB_PORT']     ?? getenv('DB_PORT')     ?: '3306';
        $dbname   = $_ENV['DB_NAME']     ?? getenv('DB_NAME')     ?: 'mydb';
        $username = $_ENV['DB_USER']     ?? getenv('DB_USER')     ?: 'root';
        $password = $_ENV['DB_PASSWORD'] ?? getenv('DB_PASSWORD') ?: '';

        $dsn = "mysql:host={$host};port={$port};dbname={$dbname};charset=utf8mb4";

        $this->connection = new PDO($dsn, $username, $password, [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);

        return $this->connection;
    }
}
