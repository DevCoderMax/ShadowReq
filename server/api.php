<?php
header('Content-Type: application/json');

// Função para realizar a requisição HTTP
function makeRequest($url, $method, $params = []) {
    $ch = curl_init();

    switch ($method) {
        case 'GET':
            if (!empty($params)) {
                $url .= '?' . http_build_query($params);
            }
            curl_setopt($ch, CURLOPT_URL, $url);
            break;
        case 'POST':
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
            break;
        case 'PUT':
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
            curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
            break;
        case 'DELETE':
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
            if (!empty($params)) {
                curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
            }
            break;
        default:
            return ['error' => 'Invalid HTTP method'];
    }

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return ['status' => $httpCode, 'response' => json_decode($response, true)];
}

// Verifica se a requisição é do tipo POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Recupera os dados da requisição
    $data = json_decode(file_get_contents('php://input'), true);
    
    // Valida os dados
    if (!isset($data['url']) || !isset($data['method'])) {
        echo json_encode(['error' => 'URL and method are required']);
        exit;
    }

    $url = $data['url'];
    $method = strtoupper($data['method']);
    $params = isset($data['params']) ? $data['params'] : [];

    // Realiza a requisição
    $result = makeRequest($url, $method, $params);

    // Retorna o resultado
    echo json_encode($result);
} else {
    echo json_encode(['error' => 'Invalid request method']);
}
?>
