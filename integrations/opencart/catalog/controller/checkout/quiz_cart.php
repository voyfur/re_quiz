<?php
/**
 * Race Expert Quiz - OpenCart Bulk Cart Controller (Customer Session Mode)
 *
 * Allows adding multiple products from a starter/training box into the buyer's
 * current OpenCart session in a single atomic HTTP request.
 *
 * Placed in catalog/controller/checkout/ so OpenCart properly binds the buyer's
 * OCSESSID cookie (in OpenCart 2.x/3.x, routes starting with 'api/' ignore cookies
 * and require an api_token).
 *
 * Route: index.php?route=checkout/quiz_cart/add_bulk
 */
class ControllerCheckoutQuizCart extends Controller {
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
                    // Call standard OpenCart cart add method with active customer session
                    $this->cart->add($product_id, $quantity, $option);
                    $added_count++;
                }
            }

            // Invalidate calculated shipping & payment cache in session
            unset($this->session->data['shipping_methods']);
            unset($this->session->data['shipping_method']);
            unset($this->session->data['payment_methods']);
            unset($this->session->data['payment_method']);

            if ($added_count > 0) {
                $json['success'] = true;
                $json['added_items'] = $added_count;
                $json['total_items'] = $this->cart->countProducts();
                $json['redirect'] = $this->url->link('checkout/cart', '', true);
            } else {
                $json['success'] = false;
                $json['error'] = 'Жоден товар зі списку не має коректного product_id';
            }
        } else {
            $json['success'] = false;
            $json['error'] = 'Порожній або некоректний список товарів для додавання';
        }

        $this->response->setOutput(json_encode($json));
    }
}
