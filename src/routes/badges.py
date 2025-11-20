# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from src.models.metrics import db, Volunteer
from datetime import datetime, timedelta
from sqlalchemy import func

badges_bp = Blueprint('badges', __name__)


@badges_bp.route('/badges/volunteer-of-week', methods=['GET'])
def get_volunteer_of_week():
    """Volontaire de la semaine - Le plus actif des 7 derniers jours"""
    try:
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Volontaire avec le plus de tâches complétées cette semaine
        top_volunteer = Volunteer.query.filter(
            Volunteer.last_seen >= week_ago
        ).order_by(
            Volunteer.tasks_completed.desc()
        ).first()
        
        if not top_volunteer:
            return jsonify({
                'success': False,
                'message': 'Aucun volontaire actif cette semaine'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'badge': 'Volontaire de la Semaine',
                'period': 'weekly',
                'volunteer': top_volunteer.to_dict(),
                'reason': f"{top_volunteer.tasks_completed} tâches complétées",
                'awarded_date': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/volunteer-of-month', methods=['GET'])
def get_volunteer_of_month():
    """Volontaire du mois - Le plus performant des 30 derniers jours"""
    try:
        month_ago = datetime.utcnow() - timedelta(days=30)
        
        # Volontaire avec le meilleur score de performance
        top_volunteer = Volunteer.query.filter(
            Volunteer.last_seen >= month_ago
        ).order_by(
            Volunteer.performance_score.desc()
        ).first()
        
        if not top_volunteer:
            return jsonify({
                'success': False,
                'message': 'Aucun volontaire actif ce mois'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'badge': 'Volontaire du Mois',
                'period': 'monthly',
                'volunteer': top_volunteer.to_dict(),
                'reason': f"Score de performance: {top_volunteer.performance_score:.1f}%",
                'awarded_date': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/volunteer-of-year', methods=['GET'])
def get_volunteer_of_year():
    """Volontaire de l'année - Le plus de temps de calcul total"""
    try:
        year_ago = datetime.utcnow() - timedelta(days=365)
        
        # Volontaire avec le plus de temps de calcul
        top_volunteer = Volunteer.query.filter(
            Volunteer.joined_date >= year_ago
        ).order_by(
            Volunteer.total_computation_time.desc()
        ).first()
        
        if not top_volunteer:
            return jsonify({
                'success': False,
                'message': 'Aucun volontaire actif cette année'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'badge': 'Volontaire de l\'Année',
                'period': 'yearly',
                'volunteer': top_volunteer.to_dict(),
                'reason': f"{top_volunteer.total_computation_time:.1f} heures de calcul",
                'awarded_date': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/top-performers', methods=['GET'])
def get_top_performers():
    """Top 10 des volontaires par catégorie"""
    try:
        category = request.args.get('category', 'all')  # all, connected, fast, tasks
        limit = int(request.args.get('limit', 10))
        
        results = {}
        
        if category in ['all', 'connected']:
            # Plus connecté (temps de calcul)
            most_connected = Volunteer.query.filter(
                Volunteer.status.in_(['active', 'busy'])
            ).order_by(
                Volunteer.total_computation_time.desc()
            ).limit(limit).all()
            
            results['most_connected'] = {
                'title': 'Plus Connecté',
                'description': 'Temps de calcul total',
                'volunteers': [v.to_dict() for v in most_connected]
            }
        
        if category in ['all', 'fast']:
            # Plus rapide (score de performance)
            fastest = Volunteer.query.filter(
                Volunteer.status.in_(['active', 'busy'])
            ).order_by(
                Volunteer.performance_score.desc()
            ).limit(limit).all()
            
            results['fastest'] = {
                'title': 'Plus Rapide',
                'description': 'Score de performance',
                'volunteers': [v.to_dict() for v in fastest]
            }
        
        if category in ['all', 'tasks']:
            # Plus de tâches
            most_tasks = Volunteer.query.order_by(
                Volunteer.tasks_completed.desc()
            ).limit(limit).all()
            
            results['most_tasks'] = {
                'title': 'Plus de Tâches',
                'description': 'Nombre de tâches complétées',
                'volunteers': [v.to_dict() for v in most_tasks]
            }
        
        return jsonify({
            'success': True,
            'data': results,
            'generated_at': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/volunteer/<volunteer_id>/badges', methods=['GET'])
def get_volunteer_badges(volunteer_id):
    """Récupère tous les badges d'un volontaire spécifique"""
    try:
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).first()
        
        if not volunteer:
            return jsonify({
                'success': False,
                'error': 'Volontaire non trouvé'
            }), 404
        
        badges = []
        
        # Badge de participation
        if volunteer.tasks_completed > 0:
            badges.append({
                'name': 'Participant Actif',
                'icon': '🎯',
                'description': f'{volunteer.tasks_completed} tâches complétées',
                'level': 'bronze' if volunteer.tasks_completed < 50 else 
                         'silver' if volunteer.tasks_completed < 200 else 'gold'
            })
        
        # Badge de performance
        if volunteer.performance_score >= 80:
            badges.append({
                'name': 'Performance Excellence',
                'icon': '⚡',
                'description': f'Score de performance: {volunteer.performance_score:.1f}%',
                'level': 'gold' if volunteer.performance_score >= 95 else 'silver'
            })
        
        # Badge de fidélité (temps de calcul)
        if volunteer.total_computation_time >= 10:
            badges.append({
                'name': 'Contributeur Fidèle',
                'icon': '⭐',
                'description': f'{volunteer.total_computation_time:.1f} heures de contribution',
                'level': 'bronze' if volunteer.total_computation_time < 50 else 
                         'silver' if volunteer.total_computation_time < 200 else 'gold'
            })
        
        # Badge de vétéran (ancienneté)
        days_active = (datetime.utcnow() - volunteer.joined_date).days if volunteer.joined_date else 0
        if days_active >= 30:
            badges.append({
                'name': 'Vétéran',
                'icon': '🏆',
                'description': f'{days_active} jours d\'ancienneté',
                'level': 'bronze' if days_active < 90 else 
                         'silver' if days_active < 365 else 'gold'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'volunteer': volunteer.to_dict(),
                'badges': badges,
                'total_badges': len(badges)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/leaderboard', methods=['GET'])
def get_leaderboard():
    """Tableau des leaders global"""
    try:
        period = request.args.get('period', 'all')  # all, week, month, year
        
        query = Volunteer.query
        
        if period == 'week':
            week_ago = datetime.utcnow() - timedelta(days=7)
            query = query.filter(Volunteer.last_seen >= week_ago)
        elif period == 'month':
            month_ago = datetime.utcnow() - timedelta(days=30)
            query = query.filter(Volunteer.last_seen >= month_ago)
        elif period == 'year':
            year_ago = datetime.utcnow() - timedelta(days=365)
            query = query.filter(Volunteer.joined_date >= year_ago)
        
        # Classement par score composite
        volunteers = query.all()
        
        # Calculer un score composite pour le classement
        leaderboard = []
        for v in volunteers:
            composite_score = (
                (v.tasks_completed * 0.4) + 
                (v.performance_score * 0.3) + 
                (v.total_computation_time * 0.3)
            )
            leaderboard.append({
                'volunteer': v.to_dict(),
                'composite_score': round(composite_score, 2)
            })
        
        # Trier par score composite
        leaderboard.sort(key=lambda x: x['composite_score'], reverse=True)
        
        # Ajouter les rangs
        for i, entry in enumerate(leaderboard[:50], 1):
            entry['rank'] = i
        
        return jsonify({
            'success': True,
            'data': {
                'period': period,
                'leaderboard': leaderboard[:50],
                'total_volunteers': len(volunteers),
                'generated_at': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


        # -*- coding: utf-8 -*-
# ... (garder tout le code existant) ...

# NOUVEAUX ENDPOINTS POUR AFFICHER LES BADGES ATTRIBUÉS

@badges_bp.route('/badges/attributed', methods=['GET'])
def get_all_attributed_badges():
    """
    Récupère tous les badges attribués (avec filtres optionnels)
    
    Query params:
    - period: week, month, year, all-time
    - volunteer_id: filtrer par volontaire
    - badge_id: filtrer par type de badge
    - limit: nombre de résultats (défaut: 50)
    - offset: pagination
    """
    try:
        from src.models.badge import VolunteerBadge, Badge
        
        # Paramètres de filtrage
        period = request.args.get('period')
        volunteer_id = request.args.get('volunteer_id')
        badge_id = request.args.get('badge_id')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        # Construire la requête
        query = VolunteerBadge.query.filter_by(revoked=False)
        
        if period:
            query = query.filter_by(period=period)
        
        if volunteer_id:
            query = query.filter_by(volunteer_id=volunteer_id)
        
        if badge_id:
            query = query.filter_by(badge_id=int(badge_id))
        
        # Trier par date (plus récents d'abord)
        query = query.order_by(VolunteerBadge.earned_date.desc())
        
        # Pagination
        total_count = query.count()
        attributed_badges = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'data': {
                'badges': [badge.to_dict() for badge in attributed_badges],
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': (offset + limit) < total_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
# badges attribues

@badges_bp.route('/badges/volunteer/<volunteer_id>/attributed', methods=['GET'])
def get_volunteer_attributed_badges(volunteer_id):
    """
    Récupère tous les badges attribués à un volontaire spécifique
    
    Query params:
    - include_revoked: inclure les badges révoqués (défaut: false)
    """
    try:
        from src.models.badge import VolunteerBadge, Badge
        from src.models.metrics import Volunteer
        
        # Vérifier que le volontaire existe
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).first()
        if not volunteer:
            return jsonify({
                'success': False,
                'error': 'Volontaire non trouvé'
            }), 404
        
        # Inclure les badges révoqués ?
        include_revoked = request.args.get('include_revoked', 'false').lower() == 'true'
        
        # Requête
        query = VolunteerBadge.query.filter_by(volunteer_id=volunteer_id)
        
        if not include_revoked:
            query = query.filter_by(revoked=False)
        
        attributed_badges = query.order_by(VolunteerBadge.earned_date.desc()).all()
        
        # Statistiques
        total_badges = len(attributed_badges)
        badges_by_period = {}
        badges_by_category = {}
        
        for badge_attr in attributed_badges:
            if not badge_attr.revoked:
                # Par période
                period = badge_attr.period or 'all-time'
                badges_by_period[period] = badges_by_period.get(period, 0) + 1
                
                # Par catégorie
                if badge_attr.badge:
                    category = badge_attr.badge.category or 'other'
                    badges_by_category[category] = badges_by_category.get(category, 0) + 1
        
        return jsonify({
            'success': True,
            'data': {
                'volunteer': volunteer.to_dict(),
                'badges': [badge.to_dict() for badge in attributed_badges],
                'statistics': {
                    'total_badges': total_badges,
                    'active_badges': sum(1 for b in attributed_badges if not b.revoked),
                    'revoked_badges': sum(1 for b in attributed_badges if b.revoked),
                    'by_period': badges_by_period,
                    'by_category': badges_by_category
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@badges_bp.route('/badges/attributed/<int:attribution_id>', methods=['GET'])
def get_attributed_badge_details(attribution_id):
    """
    Récupère les détails d'une attribution de badge spécifique
    """
    try:
        from src.models.badge import VolunteerBadge
        from src.models.metrics import Volunteer
        
        attribution = VolunteerBadge.query.get_or_404(attribution_id)
        
        # Récupérer les infos du volontaire
        volunteer = Volunteer.query.filter_by(
            volunteer_id=attribution.volunteer_id
        ).first()
        
        result = attribution.to_dict()
        if volunteer:
            result['volunteer'] = volunteer.to_dict()
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404


@badges_bp.route('/badges/attributed/recent', methods=['GET'])
def get_recent_attributed_badges():
    """
    Récupère les badges récemment attribués (dernières 24h par défaut)
    
    Query params:
    - hours: nombre d'heures (défaut: 24)
    - limit: nombre de résultats (défaut: 20)
    """
    try:
        from src.models.badge import VolunteerBadge
        from datetime import timedelta
        
        hours = int(request.args.get('hours', 24))
        limit = int(request.args.get('limit', 20))
        
        cutoff_date = datetime.utcnow() - timedelta(hours=hours)
        
        recent_badges = VolunteerBadge.query.filter(
            VolunteerBadge.earned_date >= cutoff_date,
            VolunteerBadge.revoked == False
        ).order_by(VolunteerBadge.earned_date.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'badges': [badge.to_dict() for badge in recent_badges],
                'period': f'last_{hours}_hours',
                'count': len(recent_badges)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
# badges attribues

@badges_bp.route('/badges/attributed/statistics', methods=['GET'])
def get_attribution_statistics():
    """
    Récupère les statistiques globales sur les attributions de badges
    """
    try:
        from src.models.badge import VolunteerBadge, Badge
        from sqlalchemy import func
        
        # Total d'attributions
        total_attributions = VolunteerBadge.query.filter_by(revoked=False).count()
        
        # Par période
        by_period = db.session.query(
            VolunteerBadge.period,
            func.count(VolunteerBadge.id).label('count')
        ).filter_by(revoked=False).group_by(VolunteerBadge.period).all()
        
        # Par catégorie de badge
        by_category = db.session.query(
            Badge.category,
            func.count(VolunteerBadge.id).label('count')
        ).join(VolunteerBadge).filter(
            VolunteerBadge.revoked == False
        ).group_by(Badge.category).all()
        
        # Volontaires les plus badgés
        top_volunteers = db.session.query(
            VolunteerBadge.volunteer_id,
            func.count(VolunteerBadge.id).label('badge_count')
        ).filter_by(revoked=False).group_by(
            VolunteerBadge.volunteer_id
        ).order_by(func.count(VolunteerBadge.id).desc()).limit(10).all()
        
        # Badges les plus attribués
        most_attributed = db.session.query(
            Badge.name,
            Badge.icon,
            func.count(VolunteerBadge.id).label('count')
        ).join(VolunteerBadge).filter(
            VolunteerBadge.revoked == False
        ).group_by(Badge.id).order_by(
            func.count(VolunteerBadge.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_attributions': total_attributions,
                'by_period': {period: count for period, count in by_period if period},
                'by_category': {cat: count for cat, count in by_category if cat},
                'top_volunteers': [
                    {'volunteer_id': vol_id, 'badge_count': count}
                    for vol_id, count in top_volunteers
                ],
                'most_attributed_badges': [
                    {'name': name, 'icon': icon, 'count': count}
                    for name, icon, count in most_attributed
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500