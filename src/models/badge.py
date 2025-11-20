# -*- coding: utf-8 -*-
"""
Modèles de données pour le système de badges
"""
from datetime import datetime
from src.models.metrics import db

class Badge(db.Model):
    """
    Modèle pour les types de badges disponibles
    """
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # most_connected, fastest, most_tasks, best_performance, consistency
    icon = db.Column(db.String(50), default='🏆')
    level = db.Column(db.String(50), default='bronze')  # bronze, silver, gold
    criteria = db.Column(db.JSON)  # Critères pour obtenir le badge
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertir en dictionnaire pour JSON"""
        return {
            'id': self.id,
            'badge_id': self.badge_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'level': self.level,
            'criteria': self.criteria,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class VolunteerBadge(db.Model):
    """
    Table d'association entre volontaires et badges
    Enregistre l'attribution des badges
    """
    __tablename__ = 'volunteer_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.String(100), nullable=False, index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    period = db.Column(db.String(50))  # week, month, year, all-time
    period_start = db.Column(db.DateTime)  # Début de la période
    period_end = db.Column(db.DateTime)    # Fin de la période
    reason = db.Column(db.Text)  # Raison de l'attribution
    metric_value = db.Column(db.Float)  # Valeur de la métrique (ex: 150 tâches)
    rank = db.Column(db.Integer)  # Position dans le classement
    notified = db.Column(db.Boolean, default=False)
    notification_date = db.Column(db.DateTime)
    revoked = db.Column(db.Boolean, default=False)  # Badge révoqué ?
    revoked_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    badge = db.relationship('Badge', backref='attributions', lazy='joined')
    
    def to_dict(self, include_badge=True):
        """Convertir en dictionnaire pour JSON"""
        result = {
            'id': self.id,
            'volunteer_id': self.volunteer_id,
            'badge_id': self.badge_id,
            'earned_date': self.earned_date.isoformat() if self.earned_date else None,
            'period': self.period,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'reason': self.reason,
            'metric_value': self.metric_value,
            'rank': self.rank,
            'notified': self.notified,
            'notification_date': self.notification_date.isoformat() if self.notification_date else None,
            'revoked': self.revoked,
            'revoked_date': self.revoked_date.isoformat() if self.revoked_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_badge and self.badge:
            result['badge'] = self.badge.to_dict()
        
        return result