<?php
/**
 * Race Expert Quiz - OpenCart Bulk Cart Controller
 *
 * Allows adding multiple products from a starter/training box into the buyer's
 * current OpenCart session in a single atomic HTTP request.
 *
 * Route: index.php?route=api/quiz_cart/add_bulk
 */
class ControllerApiQuizCart extends Controller {
    public function add_bulk() {
        $this->response->addHeader('Content-Type: application/json');
        $json = array();

        // Retrieve raw JSON body
        $raw_input = file_get_contents('php://input');
        $data = json_decode($raw_input, true);

        if (!empty($data['items']) && is_array($data['items'])) {
            $added_count = 0;

            foreach ($data['items'] as $item) {
                $product_id = isset($item['product_id']) ? (int)$item['product_id'] : 0;
                $quantity = isset($item['quantity']) ? (int)$item['quantity'] : 1;
                $option = isset($item['option']) && is_array($item['option']) ? $item['option'] : array();

                if ($product_id > 0 && $quantity > 0) {
                    // Call standard OpenCart cart add method
                    $this->cart->add($product_id, $quantity, $option);
                    $added_count++;
                }
            }

            // Invalidate calculated shipping & payment cache in session
            unset($this->session->data['shipping_methods']);
            unset($this->session->data['shipping_method']);
            unset($this->session->data['payment_methods']);
            unset($this->session->data['payment_method']);

            $json['success'] = true;
            $json['added_items'] = $added_count;
            $json['total_items'] = $this->cart->countProducts();
            $json['redirect'] = $this->url->link('checkout/cart', '', true);
        } else {
            $json['success'] = false;
            $json['error'] = 'Порожній або некоректний список товарів для додавання';
        }

        $this->response->setOutput(json_encode($json));
    }
}
