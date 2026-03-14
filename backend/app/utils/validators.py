from datetime import datetime
from typing import Any, Dict

class MedicalDataValidator:
    @staticmethod
    def validate_blood_pressure(systolic: int, diastolic: int) -> Dict[str, Any]:
        errors = []
        
        if not (50 <= systolic <= 250):
            errors.append("Систолическое давление должно быть между 50 и 250")
        if not (30 <= diastolic <= 150):
            errors.append("Диастолическое давление должно быть между 30 и 150")
        if systolic <= diastolic:
            errors.append("Систолическое давление должно быть больше диастолического")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_blood_glucose(value: float, unit: str = "mg/dL") -> Dict[str, Any]:
        errors = []
        
        if unit == "mg/dL":
            if not (20 <= value <= 600):
                errors.append("Уровень глюкозы должен быть между 20 и 600 mg/dL")
        elif unit == "mmol/L":
            if not (1.1 <= value <= 33.3):
                errors.append("Уровень глюкозы должен быть между 1.1 и 33.3 mmol/L")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_weight(value: float, unit: str = "kg") -> Dict[str, Any]:
        errors = []
        
        if unit == "kg":
            if not (20 <= value <= 300):
                errors.append("Вес должен быть между 20 и 300 кг")
        elif unit == "lb":
            if not (44 <= value <= 660):
                errors.append("Вес должен быть между 44 и 660 фунтов")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_date_range(start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        errors = []
        
        if start_date > end_date:
            errors.append("Дата начала не может быть позже даты окончания")
        
        max_period = 365
        if (end_date - start_date).days > max_period:
            errors.append(f"Период не может превышать {max_period} дней")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

medical_validator = MedicalDataValidator()