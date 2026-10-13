package com.cardiovision.cardiovision;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class CardioController {

	private final CardioService cardioService;

	public CardioController(CardioService cardioService) {
		this.cardioService = cardioService;
	}

	@PostMapping("/predict")
	public ResponseEntity<Map<String, Object>> predict(@RequestBody Map<String, Object> patientData) {
		return ResponseEntity.ok(cardioService.predictRisk(patientData));
	}

}
