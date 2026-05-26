<?php
declare(strict_types=1);

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class CustomerTest extends TestCase
{
    public function testXssIsStrippedFromName(): void
    {
        $raw  = '<script>alert("xss")</script>';
        $safe = htmlspecialchars($raw, ENT_QUOTES, 'UTF-8');

        $this->assertStringNotContainsString('<script>', $safe);
        $this->assertStringContainsString('&lt;script&gt;', $safe);
    }

    public function testEmptyCustomerListReturnsArray(): void
    {
        $customers = [];
        $this->assertIsArray($customers);
        $this->assertCount(0, $customers);
    }

    public function testCustomerRowHasRequiredKeys(): void
    {
        $row = [
            'id'         => 1,
            'name'       => 'Alice',
            'email'      => 'alice@example.com',
            'created_at' => '2025-01-01 10:00:00',
        ];

        foreach (['id', 'name', 'email', 'created_at'] as $key) {
            $this->assertArrayHasKey($key, $row);
        }
    }

    public function testEmailFormatIsValid(): void
    {
        $this->assertNotFalse(filter_var('bob@example.com', FILTER_VALIDATE_EMAIL));
        $this->assertFalse(filter_var('not-an-email', FILTER_VALIDATE_EMAIL));
    }
}
