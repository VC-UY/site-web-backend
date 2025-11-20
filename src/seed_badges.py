# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app, db
from src.models.badge import Badge

def seed_badges():
    """Créer les badges par défaut"""
    
    with app.app_context():
        print("🌱 Peuplement des badges par défaut...")
        print("-" * 60)
        
        # Vérifier si des badges existent déjà
        existing_count = Badge.query.count()
        if existing_count > 0:
            print(f"ℹ️  {existing_count} badges existent déjà")
            response = input("Voulez-vous les supprimer et recréer ? (y/N): ")
            if response.lower() == 'y':
                Badge.query.delete()
                db.session.commit()
                print("✅ Badges existants supprimés")
            else:
                print("❌ Opération annulée")
                return
        
        # Liste des badges par défaut
        default_badges = [
            # Badges de période
            {
                'badge_id': 'volunteer_of_week',
                'name': 'Volontaire de la Semaine',
                'description': 'Décerné au volontaire le plus actif de la semaine',
                'category': 'period',
                'icon': '🌟',
                'level': 'gold',
                'criteria': {'type': 'period', 'period': 'week'}
            },
            {
                'badge_id': 'volunteer_of_month',
                'name': 'Volontaire du Mois',
                'description': 'Décerné au volontaire le plus performant du mois',
                'category': 'period',
                'icon': '⭐',
                'level': 'gold',
                'criteria': {'type': 'period', 'period': 'month'}
            },
            {
                'badge_id': 'volunteer_of_year',
                'name': 'Volontaire de l\'Année',
                'description': 'Décerné au volontaire ayant contribué le plus durant l\'année',
                'category': 'period',
                'icon': '🏆',
                'level': 'gold',
                'criteria': {'type': 'period', 'period': 'year'}
            },
            
            # Badges de participation
            {
                'badge_id': 'participant_bronze',
                'name': 'Participant Actif - Bronze',
                'description': 'Complété 50 tâches',
                'category': 'most_tasks',
                'icon': '🎯',
                'level': 'bronze',
                'criteria': {'type': 'tasks_completed', 'min': 50, 'max': 199}
            },
            {
                'badge_id': 'participant_silver',
                'name': 'Participant Actif - Argent',
                'description': 'Complété 200 tâches',
                'category': 'most_tasks',
                'icon': '🎯',
                'level': 'silver',
                'criteria': {'type': 'tasks_completed', 'min': 200, 'max': 499}
            },
            {
                'badge_id': 'participant_gold',
                'name': 'Participant Actif - Or',
                'description': 'Complété 500 tâches ou plus',
                'category': 'most_tasks',
                'icon': '🎯',
                'level': 'gold',
                'criteria': {'type': 'tasks_completed', 'min': 500}
            },
            
            # Badges de performance
            {
                'badge_id': 'performance_silver',
                'name': 'Performance Excellence - Argent',
                'description': 'Score de performance supérieur à 80%',
                'category': 'best_performance',
                'icon': '⚡',
                'level': 'silver',
                'criteria': {'type': 'performance_score', 'min': 80, 'max': 94.9}
            },
            {
                'badge_id': 'performance_gold',
                'name': 'Performance Excellence - Or',
                'description': 'Score de performance supérieur à 95%',
                'category': 'best_performance',
                'icon': '⚡',
                'level': 'gold',
                'criteria': {'type': 'performance_score', 'min': 95}
            },
            
            # Badges de fidélité
            {
                'badge_id': 'loyalty_bronze',
                'name': 'Contributeur Fidèle - Bronze',
                'description': '50 heures de contribution',
                'category': 'most_connected',
                'icon': '⭐',
                'level': 'bronze',
                'criteria': {'type': 'computation_time', 'min': 50, 'max': 199}
            },
            {
                'badge_id': 'loyalty_silver',
                'name': 'Contributeur Fidèle - Argent',
                'description': '200 heures de contribution',
                'category': 'most_connected',
                'icon': '⭐',
                'level': 'silver',
                'criteria': {'type': 'computation_time', 'min': 200, 'max': 499}
            },
            {
                'badge_id': 'loyalty_gold',
                'name': 'Contributeur Fidèle - Or',
                'description': '500 heures de contribution ou plus',
                'category': 'most_connected',
                'icon': '⭐',
                'level': 'gold',
                'criteria': {'type': 'computation_time', 'min': 500}
            },
            
            # Badge vétéran
            {
                'badge_id': 'veteran_bronze',
                'name': 'Vétéran - Bronze',
                'description': '90 jours d\'ancienneté',
                'category': 'consistency',
                'icon': '🏅',
                'level': 'bronze',
                'criteria': {'type': 'days_active', 'min': 90, 'max': 364}
            },
            {
                'badge_id': 'veteran_silver',
                'name': 'Vétéran - Argent',
                'description': '1 an d\'ancienneté',
                'category': 'consistency',
                'icon': '🏅',
                'level': 'silver',
                'criteria': {'type': 'days_active', 'min': 365, 'max': 729}
            },
            {
                'badge_id': 'veteran_gold',
                'name': 'Vétéran - Or',
                'description': '2 ans d\'ancienneté ou plus',
                'category': 'consistency',
                'icon': '🏅',
                'level': 'gold',
                'criteria': {'type': 'days_active', 'min': 730}
            },
            
            # Badges spéciaux
            {
                'badge_id': 'top_performer',
                'name': 'Top Performer',
                'description': 'Classé dans le top 10 des volontaires',
                'category': 'fastest',
                'icon': '🚀',
                'level': 'gold',
                'criteria': {'type': 'ranking', 'max_rank': 10}
            },
            {
                'badge_id': 'speedster',
                'name': 'Speedster',
                'description': 'Temps d\'exécution moyen très rapide',
                'category': 'fastest',
                'icon': '💨',
                'level': 'gold',
                'criteria': {'type': 'avg_execution_time', 'percentile': 90}
            }
        ]
        
        # Créer les badges
        created_count = 0
        for badge_data in default_badges:
            try:
                badge = Badge(**badge_data)
                db.session.add(badge)
                created_count += 1
                print(f"✅ Badge créé: {badge.name} {badge.icon}")
            except Exception as e:
                print(f"❌ Erreur lors de la création de {badge_data['name']}: {e}")
        
        # Sauvegarder
        try:
            db.session.commit()
            print("-" * 60)
            print(f"🎉 {created_count} badges créés avec succès!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la sauvegarde: {e}")

if __name__ == '__main__':
    seed_badges()