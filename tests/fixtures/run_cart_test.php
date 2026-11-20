<?php
// Mock OpenCart Environment
class CartMock {
    public $items = [];
    public function add($p, $q = 1, $opt = []) {
        $this->items[] = ['product_id' => $p, 'quantity' => $q, 'option' => $opt];
    }
    public function countProducts() {
        $sum = 0;
        foreach ($this->items as $it) {
            $sum += $it['quantity'];
        }
        return $sum;
    }
}

class SessionMock {
    public $data = [
        'shipping_methods' => ['dummy_shipping'],
        'shipping_method' => 'np',
        'payment_methods' => ['dummy_payment'],
        'payment_method' => 'card',
        'customer_id' => 42
    ];
}

class ResponseMock {
    public $headers = [];
    public $output = '';
    public function addHeader($h) { $this->headers[] = $h; }
    public function setOutput($o) { $this->output = $o; }
}

class UrlMock {
    public function link($r, $a = '', $s = true) {
        return 'https://raceexpert.com.ua/index.php?route=' . $r;
    }
}

class Controller {
    public $cart;
    public $session;
    public $response;
    public $url;
    public function __construct() {
        $this->cart = new CartMock();
        $this->session = new SessionMock();
        $this->response = new ResponseMock();
        $this->url = new UrlMock();
    }
}

// Read raw PHP controller and inject test stream
$controller_file = '/app/catalog/controller/checkout/quiz_cart.php';
if (!file_exists($controller_file)) {
    echo "ERROR: controller file not found at " . $controller_file . "\n";
    exit(1);
}

$raw_code = file_get_contents($controller_file);
$patched_code = str_replace(
    "file_get_contents('php://input')",
    "\$GLOBALS['TEST_INPUT_PAYLOAD']",
    $raw_code
);

eval("?>" . $patched_code);

$mode = $argv[1] ?? 'valid';

if ($mode === 'valid') {
    $GLOBALS['TEST_INPUT_PAYLOAD'] = json_encode([
        'items' => [
            ['product_id' => 1940, 'quantity' => 4],
            ['product_id' => 3110, 'quantity' => 1],
            ['product_id' => 5422, 'quantity' => 2]
        ]
    ]);

    $ctrl = new ControllerCheckoutQuizCart();
    $ctrl->add_bulk();

    $res = json_decode($ctrl->response->output, true);
    if (!isset($res['success']) || $res['success'] !== true) {
        echo "FAIL: expected success=true\n";
        exit(1);
    }
    if ($res['added_items'] !== 3) {
        echo "FAIL: expected added_items=3, got " . $res['added_items'] . "\n";
        exit(1);
    }
    if ($res['total_items'] !== 7) {
        echo "FAIL: expected total_items=7 (4+1+2), got " . $res['total_items'] . "\n";
        exit(1);
    }
    if (isset($ctrl->session->data['shipping_methods']) || isset($ctrl->session->data['payment_methods'])) {
        echo "FAIL: session cache not invalidated\n";
        exit(1);
    }
    if ($ctrl->session->data['customer_id'] !== 42) {
        echo "FAIL: customer session lost\n";
        exit(1);
    }
    echo "OK_VALID\n";
    exit(0);
}

if ($mode === 'invalid_ids') {
    $GLOBALS['TEST_INPUT_PAYLOAD'] = json_encode([
        'items' => [
            ['product_id' => 0, 'quantity' => 4],
            ['product_id' => -10, 'quantity' => 1]
        ]
    ]);

    $ctrl = new ControllerCheckoutQuizCart();
    $ctrl->add_bulk();

    $res = json_decode($ctrl->response->output, true);
    if (!isset($res['success']) || $res['success'] !== false) {
        echo "FAIL: invalid IDs should return success=false\n";
        exit(1);
    }
    if (empty($res['error'])) {
        echo "FAIL: expected non-empty error message\n";
        exit(1);
    }
    echo "OK_INVALID_DETECTED\n";
    exit(0);
}

if ($mode === 'empty_payload') {
    $GLOBALS['TEST_INPUT_PAYLOAD'] = '';

    $ctrl = new ControllerCheckoutQuizCart();
    $ctrl->add_bulk();

    $res = json_decode($ctrl->response->output, true);
    if (!isset($res['success']) || $res['success'] !== false) {
        echo "FAIL: empty input should return success=false\n";
        exit(1);
    }
    echo "OK_EMPTY_DETECTED\n";
    exit(0);
}

echo "ERROR: unknown mode $mode\n";
exit(1);
