package com.cardiovision.cardiovision;

import java.util.Map;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class CardioService {

	private static final String PYTHON_PREDICT_URL = "http://127.0.0.1:8000/predict";

	private final RestTemplate restTemplate = new RestTemplate();

	public Map<String, Object> predictRisk(Map<String, Object> patientData) {
		Map<String, Object> payload = Map.of("features", patientData);
		HttpEntity<Map<String, Object>> request = new HttpEntity<>(payload);
		ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
				PYTHON_PREDICT_URL,
				HttpMethod.POST,
				request,
				new ParameterizedTypeReference<Map<String, Object>>() {
				});
		return response.getBody();
	}

}
