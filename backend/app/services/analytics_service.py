from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.repositories.measurement_repository import (
    blood_pressure_repository,
    blood_glucose_repository,
    weight_repository
)
from app.repositories.wellness_repository import wellness_repository

class AnalyticsService:
    def get_measurements_by_date_range(
        self,
        db: Session,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        measurement_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = []
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)
        bp_data = blood_pressure_repository.get_by_user(db, user_id, 0, 1000)
        bg_data = blood_glucose_repository.get_by_user(db, user_id, 0, 1000)
        weight_data = weight_repository.get_by_user(db, user_id, 0, 1000)
        wellness_data = wellness_repository.get_by_user(db, user_id, 0, 1000)
        for item in bp_data:
            item_date = item.date.replace(tzinfo=None) if item.date.tzinfo is not None else item.date
            
            if start_date <= item_date <= end_date and (not measurement_type or measurement_type == 'blood_pressure'):
                results.append({
                    "type": "blood_pressure",
                    "date": item.date,
                    "systolic": item.systolic,
                    "diastolic": item.diastolic,
                    "pulse": item.pulse if hasattr(item, 'pulse') else None,
                    "notes": item.notes
                })
        
        for item in bg_data:
            item_date = item.date.replace(tzinfo=None) if item.date.tzinfo is not None else item.date
            
            if start_date <= item_date <= end_date and (not measurement_type or measurement_type == 'blood_glucose'):
                results.append({
                    "type": "blood_glucose",
                    "date": item.date,
                    "value": item.value,
                    "unit": item.unit,
                    "notes": item.notes
                })
        
        for item in weight_data:
            item_date = item.date.replace(tzinfo=None) if item.date.tzinfo is not None else item.date
            
            if start_date <= item_date <= end_date and (not measurement_type or measurement_type == 'weight'):
                results.append({
                    "type": "weight",
                    "date": item.date,
                    "value": item.value,
                    "unit": item.unit,
                    "notes": item.notes
                })
        
        for item in wellness_data:
            item_date = item.date.replace(tzinfo=None) if item.date.tzinfo is not None else item.date
            
            if start_date <= item_date <= end_date and (not measurement_type or measurement_type == 'wellness'):
                results.append({
                    "type": "wellness",
                    "date": item.date,
                    "description": item.description,
                    "mood": item.mood,
                    "symptoms": item.symptoms
                })
        results.sort(key=lambda x: x['date'])
        return results
    
    def get_measurements_stats(
        self,
        db: Session,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        
        measurements = self.get_measurements_by_date_range(db, user_id, start_date, end_date)
        stats = {
            "blood_pressure": {"systolic": [], "diastolic": [], "pulse": []},
            "blood_glucose": [],
            "weight": [],
            "wellness_entries": 0
        }
        
        for measurement in measurements:
            if measurement['type'] == 'blood_pressure':
                if measurement['systolic']:
                    stats['blood_pressure']['systolic'].append(measurement['systolic'])
                if measurement['diastolic']:
                    stats['blood_pressure']['diastolic'].append(measurement['diastolic'])
                if measurement.get('pulse'):
                    stats['blood_pressure']['pulse'].append(measurement['pulse'])
            elif measurement['type'] == 'blood_glucose':
                stats['blood_glucose'].append(measurement['value'])
            elif measurement['type'] == 'weight':
                stats['weight'].append(measurement['value'])
            elif measurement['type'] == 'wellness':
                stats['wellness_entries'] += 1
        for key in ['blood_pressure', 'blood_glucose', 'weight']:
            if key == 'blood_pressure':
                for subkey in ['systolic', 'diastolic', 'pulse']:
                    if stats[key][subkey]:
                        stats[key][f'avg_{subkey}'] = sum(stats[key][subkey]) / len(stats[key][subkey])
                        stats[key][f'min_{subkey}'] = min(stats[key][subkey])
                        stats[key][f'max_{subkey}'] = max(stats[key][subkey])
            else:
                if stats[key]:
                    stats[key] = {
                        'values': stats[key],
                        'avg': sum(stats[key]) / len(stats[key]),
                        'min': min(stats[key]),
                        'max': max(stats[key])
                    }
        
        return stats
    
    def get_dashboard_data(
        self,
        db: Session,
        user_id: int
    ) -> Dict[str, Any]:
        """Получение данных для главной страницы"""
        bp_data = blood_pressure_repository.get_by_user(db, user_id, 0, 1)
        bg_data = blood_glucose_repository.get_by_user(db, user_id, 0, 1)
        weight_data = weight_repository.get_by_user(db, user_id, 0, 1)
        
        return {
            "latest_blood_pressure": bp_data[0] if bp_data else None,
            "latest_blood_glucose": bg_data[0] if bg_data else None,
            "latest_weight": weight_data[0] if weight_data else None,
            "weekly_stats": self.get_measurements_stats(db, user_id, 7)
        }

analytics_service = AnalyticsService()