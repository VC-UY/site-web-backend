from flask import Blueprint, jsonify, request
from src.models.metrics import db, SystemMetrics, Volunteer, Task, PerformanceHistory
from datetime import datetime, timedelta
import random

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/system-metrics', methods=['GET'])
def get_system_metrics():
    """Récupère les métriques système en temps réel"""
    try:
        # Récupérer les dernières métriques ou générer des données de démonstration
        latest_metrics = SystemMetrics.query.order_by(SystemMetrics.timestamp.desc()).first()
        
        if not latest_metrics:
            # Générer des données de démonstration
            demo_metrics = SystemMetrics(
                total_volunteers=random.randint(50, 150),
                active_volunteers=random.randint(20, 80),
                total_tasks=random.randint(1000, 5000),
                completed_tasks=random.randint(800, 4500),
                pending_tasks=random.randint(50, 500),
                cpu_usage=random.uniform(30.0, 85.0),
                memory_usage=random.uniform(40.0, 90.0),
                network_throughput=random.uniform(100.0, 1000.0),
                cost_savings=random.uniform(10000.0, 50000.0)
            )
            db.session.add(demo_metrics)
            db.session.commit()
            latest_metrics = demo_metrics
        
        return jsonify({
            'success': True,
            'data': latest_metrics.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/volunteers', methods=['GET'])
def get_volunteers():
    """Récupère la liste des volontaires et leurs performances"""
    try:
        volunteers = Volunteer.query.all()
        
        # Si aucun volontaire, générer des données de démonstration
        if not volunteers:
            demo_volunteers = [
                Volunteer(
                    volunteer_id=f"vol_{i:03d}",
                    name=f"Volontaire {i}",
                    status=random.choice(['active', 'inactive', 'busy']),
                    tasks_completed=random.randint(10, 200),
                    total_computation_time=random.uniform(5.0, 100.0),
                    cpu_cores=random.choice([2, 4, 8, 16]),
                    memory_gb=random.choice([4.0, 8.0, 16.0, 32.0]),
                    performance_score=random.uniform(70.0, 95.0)
                ) for i in range(1, 21)
            ]
            
            for vol in demo_volunteers:
                db.session.add(vol)
            db.session.commit()
            volunteers = demo_volunteers
        
        return jsonify({
            'success': True,
            'data': [vol.to_dict() for vol in volunteers]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/volunteers/<volunteer_id>', methods=['GET'])
def get_volunteer_details(volunteer_id):
    """Récupère les détails d'un volontaire spécifique"""
    try:
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).first()
        
        if not volunteer:
            return jsonify({
                'success': False,
                'error': 'Volontaire non trouvé'
            }), 404
        
        # Récupérer l'historique des performances
        performance_history = PerformanceHistory.query.filter_by(
            volunteer_id=volunteer_id
        ).order_by(PerformanceHistory.timestamp.desc()).limit(50).all()
        
        return jsonify({
            'success': True,
            'data': {
                'volunteer': volunteer.to_dict(),
                'performance_history': [perf.to_dict() for perf in performance_history]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Récupère la liste des tâches"""
    try:
        status_filter = request.args.get('status')
        limit = int(request.args.get('limit', 100))
        
        query = Task.query
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        tasks = query.order_by(Task.created_date.desc()).limit(limit).all()
        
        # Si aucune tâche, générer des données de démonstration
        if not tasks:
            demo_tasks = [
                Task(
                    task_id=f"task_{i:04d}",
                    workflow_id=f"workflow_{random.randint(1, 10):02d}",
                    status=random.choice(['pending', 'running', 'completed', 'failed']),
                    assigned_volunteer=f"vol_{random.randint(1, 20):03d}" if random.random() > 0.3 else None,
                    execution_time=random.uniform(10.0, 3600.0),
                    cpu_usage=random.uniform(20.0, 95.0),
                    memory_usage=random.uniform(30.0, 80.0)
                ) for i in range(1, 101)
            ]
            
            for task in demo_tasks:
                db.session.add(task)
            db.session.commit()
            tasks = demo_tasks[:limit]
        
        return jsonify({
            'success': True,
            'data': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/analytics/performance-history', methods=['GET'])
def get_performance_analytics():
    """Récupère l'historique des performances pour les analyses"""
    try:
        days = int(request.args.get('days', 7))
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Récupérer les métriques système historiques
        metrics_history = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= start_date
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        # Si pas d'historique, générer des données de démonstration
        if not metrics_history:
            demo_history = []
            for i in range(days * 24):  # Une entrée par heure
                timestamp = start_date + timedelta(hours=i)
                demo_metrics = SystemMetrics(
                    timestamp=timestamp,
                    total_volunteers=random.randint(50, 150),
                    active_volunteers=random.randint(20, 80),
                    total_tasks=random.randint(1000, 5000),
                    completed_tasks=random.randint(800, 4500),
                    pending_tasks=random.randint(50, 500),
                    cpu_usage=random.uniform(30.0, 85.0),
                    memory_usage=random.uniform(40.0, 90.0),
                    network_throughput=random.uniform(100.0, 1000.0),
                    cost_savings=random.uniform(10000.0, 50000.0)
                )
                demo_history.append(demo_metrics)
                db.session.add(demo_metrics)
            
            db.session.commit()
            metrics_history = demo_history
        
        return jsonify({
            'success': True,
            'data': [metrics.to_dict() for metrics in metrics_history]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/analytics/cost-savings', methods=['GET'])
def get_cost_savings_analytics():
    """Récupère les analyses d'économies de coûts"""
    try:
        # Calculer les économies de coûts basées sur les tâches complétées
        completed_tasks = Task.query.filter_by(status='completed').count()
        
        # Estimation du coût par tâche sur infrastructure traditionnelle
        cost_per_task_traditional = 0.50  # $0.50 par tâche
        cost_per_task_volunteer = 0.05    # $0.05 par tâche (coûts de coordination)
        
        total_traditional_cost = completed_tasks * cost_per_task_traditional
        total_volunteer_cost = completed_tasks * cost_per_task_volunteer
        total_savings = total_traditional_cost - total_volunteer_cost
        
        savings_percentage = (total_savings / total_traditional_cost * 100) if total_traditional_cost > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'completed_tasks': completed_tasks,
                'traditional_cost': total_traditional_cost,
                'volunteer_cost': total_volunteer_cost,
                'total_savings': total_savings,
                'savings_percentage': savings_percentage,
                'cost_per_task_saved': cost_per_task_traditional - cost_per_task_volunteer
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/analytics/volunteer-performance', methods=['GET'])
def get_volunteer_performance_analytics():
    """Récupère les analyses de performance des volontaires"""
    try:
        # Top 10 des volontaires par nombre de tâches complétées
        top_volunteers = Volunteer.query.order_by(
            Volunteer.tasks_completed.desc()
        ).limit(10).all()
        
        # Statistiques globales des volontaires
        total_volunteers = Volunteer.query.count()
        active_volunteers = Volunteer.query.filter_by(status='active').count()
        avg_performance = db.session.query(db.func.avg(Volunteer.performance_score)).scalar() or 0
        total_computation_hours = db.session.query(db.func.sum(Volunteer.total_computation_time)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'top_volunteers': [vol.to_dict() for vol in top_volunteers],
                'statistics': {
                    'total_volunteers': total_volunteers,
                    'active_volunteers': active_volunteers,
                    'average_performance_score': round(avg_performance, 2),
                    'total_computation_hours': round(total_computation_hours, 2),
                    'activity_rate': round((active_volunteers / total_volunteers * 100), 2) if total_volunteers > 0 else 0
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
def get_date_range(period, start_date=None, end_date=None):
    """Calcule la plage de dates selon la période"""
    now = datetime.utcnow()
    
    if period == 'hour':
        return now - timedelta(hours=1), now
    elif period == 'day':
        return now - timedelta(days=1), now
    elif period == 'week':
        return now - timedelta(weeks=1), now
    elif period == 'month':
        return now - timedelta(days=30), now
    elif period == 'year':
        return now - timedelta(days=365), now
    elif period == 'custom':
        return datetime.fromisoformat(start_date), datetime.fromisoformat(end_date)
    else:
        return now - timedelta(days=1), now

def calculate_aggregations(metrics_list, field_name):
    """Calcule les agrégations pour un champ donné"""
    if not metrics_list:
        return {
            'average': 0,
            'min': 0,
            'max': 0,
            'total': 0,
            'count': 0
        }
    
    values = [getattr(m, field_name, 0) for m in metrics_list]
    
    return {
        'average': round(sum(values) / len(values), 2),
        'min': round(min(values), 2),
        'max': round(max(values), 2),
        'total': round(sum(values), 2),
        'count': len(values)
    }

def calculate_trend(metrics_list, field_name):
    """Calcule la tendance (croissance/décroissance) d'un champ"""
    if len(metrics_list) < 2:
        return {'trend': 'stable', 'percentage': 0}
    
    first_value = getattr(metrics_list[0], field_name, 0)
    last_value = getattr(metrics_list[-1], field_name, 0)
    
    if first_value == 0:
        return {'trend': 'stable', 'percentage': 0}
    
    percentage_change = ((last_value - first_value) / first_value) * 100
    
    if percentage_change > 5:
        trend = 'increasing'
    elif percentage_change < -5:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'trend': trend,
        'percentage': round(percentage_change, 2),
        'first_value': round(first_value, 2),
        'last_value': round(last_value, 2)
    }



@metrics_bp.route('/performance/global', methods=['GET'])
def get_global_performance_metrics():
    """
    Récupère les métriques globales de performance (CPU, mémoire, réseau)
    avec filtres par période et agrégations (moyennes, pics, tendances)
    
    Query params:
    - period: hour|day|week|month|year|custom (défaut: day)
    - start_date: date de début (format ISO YYYY-MM-DD) pour période custom
    - end_date: date de fin (format ISO YYYY-MM-DD) pour période custom
    - include_trends: true|false (défaut: true)
    """
    try:
        period = request.args.get('period', 'day')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        include_trends = request.args.get('include_trends', 'true').lower() == 'true'
        
        # Calculer la plage de dates
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        # Récupérer les métriques de la période
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée disponible pour cette période'
            }), 404
        
        # Construire la réponse avec agrégations
        response_data = {
            'period': {
                'type': period,
                'start': date_start.isoformat(),
                'end': date_end.isoformat(),
                'data_points': len(metrics)
            },
            'cpu': calculate_aggregations(metrics, 'cpu_usage'),
            'memory': calculate_aggregations(metrics, 'memory_usage'),
            'network': calculate_aggregations(metrics, 'network_throughput'),
            'volunteers': {
                'total': calculate_aggregations(metrics, 'total_volunteers'),
                'active': calculate_aggregations(metrics, 'active_volunteers')
            },
            'tasks': {
                'total': calculate_aggregations(metrics, 'total_tasks'),
                'completed': calculate_aggregations(metrics, 'completed_tasks'),
                'pending': calculate_aggregations(metrics, 'pending_tasks')
            },
            'cost_savings': calculate_aggregations(metrics, 'cost_savings')
        }
        
        # Ajouter les tendances si demandé
        if include_trends:
            response_data['trends'] = {
                'cpu': calculate_trend(metrics, 'cpu_usage'),
                'memory': calculate_trend(metrics, 'memory_usage'),
                'network': calculate_trend(metrics, 'network_throughput'),
                'active_volunteers': calculate_trend(metrics, 'active_volunteers'),
                'completed_tasks': calculate_trend(metrics, 'completed_tasks')
            }
        
        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/cpu', methods=['GET'])
def get_cpu_performance():
    """
    Récupère les métriques CPU détaillées avec agrégations et pics
    
    Query params:
    - period: hour|day|week|month|year|custom
    - start_date, end_date: pour période custom
    """
    try:
        period = request.args.get('period', 'day')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée CPU disponible'
            }), 404
        
        # Points de données
        data_points = [
            {
                'timestamp': m.timestamp.isoformat(),
                'cpu_usage': m.cpu_usage
            } for m in metrics
        ]
        
        # Identifier les pics (> 80%)
        peaks = [
            {
                'timestamp': m.timestamp.isoformat(),
                'value': m.cpu_usage
            } for m in metrics if m.cpu_usage > 80
        ]
        
        response = {
            'success': True,
            'data': {
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'aggregations': calculate_aggregations(metrics, 'cpu_usage'),
                'trend': calculate_trend(metrics, 'cpu_usage'),
                'peaks': {
                    'count': len(peaks),
                    'events': peaks[:20]  # Limiter à 20 pics
                },
                'data_points': data_points
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/memory', methods=['GET'])
def get_memory_performance():
    """
    Récupère les métriques mémoire détaillées avec agrégations et alertes
    """
    try:
        period = request.args.get('period', 'day')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée mémoire disponible'
            }), 404
        
        data_points = [
            {
                'timestamp': m.timestamp.isoformat(),
                'memory_usage': m.memory_usage
            } for m in metrics
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'aggregations': calculate_aggregations(metrics, 'memory_usage'),
                'trend': calculate_trend(metrics, 'memory_usage'),
                'data_points': data_points,
                'alerts': {
                    'high_usage_count': len([m for m in metrics if m.memory_usage > 85]),
                    'critical_usage_count': len([m for m in metrics if m.memory_usage > 95])
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/network', methods=['GET'])
def get_network_performance():
    """
    Récupère les métriques réseau avec throughput
    """
    try:
        period = request.args.get('period', 'day')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée réseau disponible'
            }), 404
        
        data_points = [
            {
                'timestamp': m.timestamp.isoformat(),
                'throughput_mbps': m.network_throughput
            } for m in metrics
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'throughput': calculate_aggregations(metrics, 'network_throughput'),
                'trend': calculate_trend(metrics, 'network_throughput'),
                'data_points': data_points
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/summary', methods=['GET'])
def get_performance_summary():
    """
    Récupère un résumé complet des performances système
    Idéal pour les dashboards
    """
    try:
        # Métriques actuelles
        current = SystemMetrics.query.order_by(SystemMetrics.timestamp.desc()).first()
        
        # Métriques dernières 24h
        day_ago = datetime.utcnow() - timedelta(days=1)
        day_metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= day_ago
        ).all()
        
        # Métriques dernière semaine
        week_ago = datetime.utcnow() - timedelta(weeks=1)
        week_metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= week_ago
        ).all()
        
        if not current:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée disponible'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'current': current.to_dict(),
                'last_24h': {
                    'cpu': calculate_aggregations(day_metrics, 'cpu_usage'),
                    'memory': calculate_aggregations(day_metrics, 'memory_usage'),
                    'network': calculate_aggregations(day_metrics, 'network_throughput')
                },
                'last_week': {
                    'cpu': calculate_aggregations(week_metrics, 'cpu_usage'),
                    'memory': calculate_aggregations(week_metrics, 'memory_usage'),
                    'network': calculate_aggregations(week_metrics, 'network_throughput'),
                    'trends': {
                        'cpu': calculate_trend(week_metrics, 'cpu_usage'),
                        'memory': calculate_trend(week_metrics, 'memory_usage')
                    }
                },
                'health_score': {
                    'cpu': 'good' if current.cpu_usage < 70 else 'warning' if current.cpu_usage < 85 else 'critical',
                    'memory': 'good' if current.memory_usage < 70 else 'warning' if current.memory_usage < 85 else 'critical'
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/peaks', methods=['GET'])
def get_performance_peaks():
    """
    Identifie les pics de performance (CPU, mémoire) sur une période
    
    Query params:
    - period: hour|day|week|month|year|custom
    - threshold: seuil pour identifier un pic (défaut: 80)
    """
    try:
        period = request.args.get('period', 'week')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        threshold = float(request.args.get('threshold', 80))
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).order_by(SystemMetrics.timestamp.asc()).all()
        
        # Identifier les pics
        cpu_peaks = [m for m in metrics if m.cpu_usage >= threshold]
        memory_peaks = [m for m in metrics if m.memory_usage >= threshold]
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'threshold': threshold,
                'cpu_peaks': {
                    'count': len(cpu_peaks),
                    'highest': max([m.cpu_usage for m in cpu_peaks]) if cpu_peaks else 0,
                    'events': [
                        {
                            'timestamp': m.timestamp.isoformat(),
                            'value': m.cpu_usage
                        } for m in sorted(cpu_peaks, key=lambda x: x.cpu_usage, reverse=True)[:10]
                    ]
                },
                'memory_peaks': {
                    'count': len(memory_peaks),
                    'highest': max([m.memory_usage for m in memory_peaks]) if memory_peaks else 0,
                    'events': [
                        {
                            'timestamp': m.timestamp.isoformat(),
                            'value': m.memory_usage
                        } for m in sorted(memory_peaks, key=lambda x: x.memory_usage, reverse=True)[:10]
                    ]
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/comparison', methods=['GET'])
def compare_performance_periods():
    """
    Compare les performances entre deux périodes
    
    Query params:
    - period1_start, period1_end: première période (format ISO)
    - period2_start, period2_end: deuxième période (format ISO)
    """
    try:
        # Période 1
        p1_start = datetime.fromisoformat(request.args.get('period1_start'))
        p1_end = datetime.fromisoformat(request.args.get('period1_end'))
        
        # Période 2
        p2_start = datetime.fromisoformat(request.args.get('period2_start'))
        p2_end = datetime.fromisoformat(request.args.get('period2_end'))
        
        # Récupérer les métriques
        period1_metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= p1_start,
            SystemMetrics.timestamp <= p1_end
        ).all()
        
        period2_metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= p2_start,
            SystemMetrics.timestamp <= p2_end
        ).all()
        
        if not period1_metrics or not period2_metrics:
            return jsonify({
                'success': False,
                'error': 'Données insuffisantes pour la comparaison'
            }), 404
        
        def compare_metric(metrics1, metrics2, field):
            agg1 = calculate_aggregations(metrics1, field)
            agg2 = calculate_aggregations(metrics2, field)
            
            diff = agg2['average'] - agg1['average']
            pct_change = (diff / agg1['average'] * 100) if agg1['average'] != 0 else 0
            
            return {
                'period1': agg1,
                'period2': agg2,
                'difference': round(diff, 2),
                'percentage_change': round(pct_change, 2),
                'improved': diff < 0 if field in ['cpu_usage', 'memory_usage'] else diff > 0
            }
        
        return jsonify({
            'success': True,
            'data': {
                'periods': {
                    'period1': {
                        'start': p1_start.isoformat(),
                        'end': p1_end.isoformat(),
                        'data_points': len(period1_metrics)
                    },
                    'period2': {
                        'start': p2_start.isoformat(),
                        'end': p2_end.isoformat(),
                        'data_points': len(period2_metrics)
                    }
                },
                'comparison': {
                    'cpu': compare_metric(period1_metrics, period2_metrics, 'cpu_usage'),
                    'memory': compare_metric(period1_metrics, period2_metrics, 'memory_usage'),
                    'network': compare_metric(period1_metrics, period2_metrics, 'network_throughput'),
                    'active_volunteers': compare_metric(period1_metrics, period2_metrics, 'active_volunteers'),
                    'completed_tasks': compare_metric(period1_metrics, period2_metrics, 'completed_tasks')
                }
            }
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Format de date invalide. Utilisez le format ISO (YYYY-MM-DD)'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/alerts', methods=['GET'])
def get_performance_alerts():
    """
    Génère des alertes basées sur les seuils de performance
    
    Query params:
    - cpu_threshold: seuil CPU (défaut: 85)
    - memory_threshold: seuil mémoire (défaut: 85)
    - hours: période à analyser en heures (défaut: 24)
    """
    try:
        cpu_threshold = float(request.args.get('cpu_threshold', 85))
        memory_threshold = float(request.args.get('memory_threshold', 85))
        hours = int(request.args.get('hours', 24))
        
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= start_time
        ).order_by(SystemMetrics.timestamp.desc()).all()
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée pour générer des alertes'
            }), 404
        
        # Identifier les alertes CPU
        cpu_alerts = [
            {
                'timestamp': m.timestamp.isoformat(),
                'value': m.cpu_usage,
                'severity': 'critical' if m.cpu_usage > 95 else 'warning'
            } for m in metrics if m.cpu_usage >= cpu_threshold
        ]
        
        # Identifier les alertes mémoire
        memory_alerts = [
            {
                'timestamp': m.timestamp.isoformat(),
                'value': m.memory_usage,
                'severity': 'critical' if m.memory_usage > 95 else 'warning'
            } for m in metrics if m.memory_usage >= memory_threshold
        ]
        
        # Volontaires inactifs (plus de 24h)
        inactive_volunteers = Volunteer.query.filter(
            Volunteer.last_seen < datetime.utcnow() - timedelta(hours=24),
            Volunteer.status != 'inactive'
        ).all()
        
        # Tâches en échec
        failed_tasks = Task.query.filter(
            Task.status == 'failed',
            Task.completed_date >= start_time
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'hours': hours,
                    'start': start_time.isoformat()
                },
                'thresholds': {
                    'cpu': cpu_threshold,
                    'memory': memory_threshold
                },
                'alerts': {
                    'cpu': {
                        'count': len(cpu_alerts),
                        'events': cpu_alerts[:20]
                    },
                    'memory': {
                        'count': len(memory_alerts),
                        'events': memory_alerts[:20]
                    },
                    'inactive_volunteers': {
                        'count': len(inactive_volunteers),
                        'volunteers': [v.volunteer_id for v in inactive_volunteers[:10]]
                    },
                    'failed_tasks': {
                        'count': failed_tasks
                    }
                },
                'overall_health': 'critical' if (len(cpu_alerts) > 10 or len(memory_alerts) > 10) else 'warning' if (len(cpu_alerts) > 0 or len(memory_alerts) > 0) else 'good'
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/report', methods=['GET'])
def generate_performance_report():
    """
    Génère un rapport complet de performance pour une période donnée
    avec recommandations automatiques
    
    Query params:
    - period: hour|day|week|month|year|custom
    - start_date, end_date: pour période custom
    """
    try:
        period = request.args.get('period', 'week')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        # Récupérer toutes les données nécessaires
        metrics = SystemMetrics.query.filter(
            SystemMetrics.timestamp >= date_start,
            SystemMetrics.timestamp <= date_end
        ).all()
        
        tasks = Task.query.filter(
            Task.created_date >= date_start,
            Task.created_date <= date_end
        ).all()
        
        volunteers = Volunteer.query.all()
        active_volunteers = [v for v in volunteers if v.status == 'active']
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée pour générer le rapport'
            }), 404
        
        # Compiler le rapport
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'period': {
                'type': period,
                'start': date_start.isoformat(),
                'end': date_end.isoformat(),
                'duration_hours': (date_end - date_start).total_seconds() / 3600
            },
            'executive_summary': {
                'total_volunteers': len(volunteers),
                'active_volunteers': len(active_volunteers),
                'total_tasks': len(tasks),
                'completed_tasks': len([t for t in tasks if t.status == 'completed']),
                'failed_tasks': len([t for t in tasks if t.status == 'failed']),
                'avg_cpu_usage': round(sum([m.cpu_usage for m in metrics]) / len(metrics), 2),
                'avg_memory_usage': round(sum([m.memory_usage for m in metrics]) / len(metrics), 2)
            },
            'system_performance': {
                'cpu': calculate_aggregations(metrics, 'cpu_usage'),
                'memory': calculate_aggregations(metrics, 'memory_usage'),
                'network': calculate_aggregations(metrics, 'network_throughput'),
                'trends': {
                    'cpu': calculate_trend(metrics, 'cpu_usage'),
                    'memory': calculate_trend(metrics, 'memory_usage')
                }
            },
            'task_performance': {
                'total': len(tasks),
                'by_status': {
                    'pending': len([t for t in tasks if t.status == 'pending']),
                    'running': len([t for t in tasks if t.status == 'running']),
                    'completed': len([t for t in tasks if t.status == 'completed']),
                    'failed': len([t for t in tasks if t.status == 'failed'])
                },
                'execution_time': calculate_aggregations([t for t in tasks if t.status == 'completed'], 'execution_time')
            },
            'volunteer_performance': {
                'total': len(volunteers),
                'active': len(active_volunteers),
                'top_performers': [
                    {
                        'volunteer_id': v.volunteer_id,
                        'name': v.name,
                        'tasks_completed': v.tasks_completed,
                        'performance_score': v.performance_score
                    } for v in sorted(volunteers, key=lambda x: x.performance_score, reverse=True)[:5]
                ]
            },
            'recommendations': []
        }
        
        # Ajouter des recommandations basées sur les données
        avg_cpu = report['executive_summary']['avg_cpu_usage']
        avg_memory = report['executive_summary']['avg_memory_usage']
        failure_rate = (report['executive_summary']['failed_tasks'] / len(tasks) * 100) if tasks else 0
        
        if avg_cpu > 80:
            report['recommendations'].append({
                'type': 'warning',
                'category': 'cpu',
                'message': f'Utilisation CPU élevée ({avg_cpu}%). Envisager d\'ajouter plus de ressources.'
            })
        
        if avg_memory > 80:
            report['recommendations'].append({
                'type': 'warning',
                'category': 'memory',
                'message': f'Utilisation mémoire élevée ({avg_memory}%). Optimisation recommandée.'
            })
        
        if failure_rate > 10:
            report['recommendations'].append({
                'type': 'critical',
                'category': 'tasks',
                'message': f'Taux d\'échec élevé ({failure_rate:.2f}%). Vérifier la stabilité du système.'
            })
        
        if len(active_volunteers) < len(volunteers) * 0.5:
            report['recommendations'].append({
                'type': 'info',
                'category': 'volunteers',
                'message': 'Moins de 50% des volontaires sont actifs. Envisager une campagne de réactivation.'
            })
        
        return jsonify({
            'success': True,
            'data': report
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/volunteers/<volunteer_id>', methods=['GET'])
def get_volunteer_performance_details(volunteer_id):
    """
    Récupère les performances détaillées d'un volontaire spécifique
    avec agrégations et tendances
    
    Query params:
    - period: hour|day|week|month|year|custom
    """
    try:
        period = request.args.get('period', 'week')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        # Vérifier que le volontaire existe
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).first()
        if not volunteer:
            return jsonify({
                'success': False,
                'error': 'Volontaire non trouvé'
            }), 404
        
        # Récupérer l'historique de performances
        perf_history = PerformanceHistory.query.filter(
            PerformanceHistory.volunteer_id == volunteer_id,
            PerformanceHistory.timestamp >= date_start,
            PerformanceHistory.timestamp <= date_end
        ).order_by(PerformanceHistory.timestamp.asc()).all()
        
        if not perf_history:
            return jsonify({
                'success': False,
                'error': 'Aucune donnée de performance pour cette période'
            }), 404
        
        # Calculer les agrégations
        total_tasks = len(perf_history)
        successful_tasks = len([p for p in perf_history if p.success])
        failed_tasks = total_tasks - successful_tasks
        
        return jsonify({
            'success': True,
            'data': {
                'volunteer': volunteer.to_dict(),
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'summary': {
                    'total_tasks': total_tasks,
                    'successful_tasks': successful_tasks,
                    'failed_tasks': failed_tasks,
                    'success_rate': round((successful_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
                },
                'performance': {
                    'execution_time': calculate_aggregations(perf_history, 'execution_time'),
                    'cpu_usage': calculate_aggregations(perf_history, 'cpu_usage'),
                    'memory_usage': calculate_aggregations(perf_history, 'memory_usage')
                },
                'trends': {
                    'execution_time': calculate_trend(perf_history, 'execution_time'),
                    'cpu_usage': calculate_trend(perf_history, 'cpu_usage')
                },
                'recent_tasks': [
                    {
                        'task_id': p.task_id,
                        'timestamp': p.timestamp.isoformat(),
                        'execution_time': p.execution_time,
                        'success': p.success
                    } for p in perf_history[-10:]
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/volunteers/ranking', methods=['GET'])
def get_volunteers_performance_ranking():
    """
    Classe les volontaires par performance
    
    Query params:
    - metric: tasks_completed|performance_score|total_computation_time (défaut: performance_score)
    - limit: nombre de résultats (défaut: 20)
    - order: asc|desc (défaut: desc)
    """
    try:
        metric = request.args.get('metric', 'performance_score')
        limit = int(request.args.get('limit', 20))
        order = request.args.get('order', 'desc')
        
        # Valider le metric
        valid_metrics = ['tasks_completed', 'performance_score', 'total_computation_time']
        if metric not in valid_metrics:
            return jsonify({
                'success': False,
                'error': f'Metric invalide. Valeurs acceptées: {", ".join(valid_metrics)}'
            }), 400
        
        # Construire la requête
        query = Volunteer.query
        
        if order == 'desc':
            query = query.order_by(getattr(Volunteer, metric).desc())
        else:
            query = query.order_by(getattr(Volunteer, metric).asc())
        
        volunteers = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'ranking_by': metric,
                'order': order,
                'total_volunteers': Volunteer.query.count(),
                'results': [
                    {
                        'rank': idx + 1,
                        'volunteer': vol.to_dict(),
                        'metric_value': getattr(vol, metric)
                    } for idx, vol in enumerate(volunteers)
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/tasks/statistics', methods=['GET'])
def get_tasks_performance_statistics():
    """
    Récupère les statistiques de performance des tâches
    """
    try:
        period = request.args.get('period', 'week')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        date_start, date_end = get_date_range(period, start_date, end_date)
        
        # Récupérer les tâches de la période
        tasks = Task.query.filter(
            Task.created_date >= date_start,
            Task.created_date <= date_end
        ).all()
        
        if not tasks:
            return jsonify({
                'success': False,
                'error': 'Aucune tâche pour cette période'
            }), 404
        
        # Statistiques par statut
        status_counts = {
            'pending': len([t for t in tasks if t.status == 'pending']),
            'running': len([t for t in tasks if t.status == 'running']),
            'completed': len([t for t in tasks if t.status == 'completed']),
            'failed': len([t for t in tasks if t.status == 'failed'])
        }
        
        # Tâches complétées uniquement
        completed_tasks = [t for t in tasks if t.status == 'completed']
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start': date_start.isoformat(),
                    'end': date_end.isoformat()
                },
                'total_tasks': len(tasks),
                'status_distribution': status_counts,
                'completion_rate': round((status_counts['completed'] / len(tasks) * 100), 2) if tasks else 0,
                'failure_rate': round((status_counts['failed'] / len(tasks) * 100), 2) if tasks else 0,
                'performance': {
                    'execution_time': calculate_aggregations(completed_tasks, 'execution_time') if completed_tasks else {},
                    'cpu_usage': calculate_aggregations(completed_tasks, 'cpu_usage') if completed_tasks else {},
                    'memory_usage': calculate_aggregations(completed_tasks, 'memory_usage') if completed_tasks else {}
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@metrics_bp.route('/performance/tasks/slowest', methods=['GET'])
def get_slowest_tasks():
    """
    Identifie les tâches les plus lentes
    
    Query params:
    - limit: nombre de résultats (défaut: 10)
    - min_execution_time: temps minimum en secondes (défaut: 0)
    """
    try:
        limit = int(request.args.get('limit', 10))
        min_time = float(request.args.get('min_execution_time', 0))
        
        tasks = Task.query.filter(
            Task.status == 'completed',
            Task.execution_time >= min_time
        ).order_by(Task.execution_time.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_found': len(tasks),
                'tasks': [
                    {
                        'task_id': t.task_id,
                        'workflow_id': t.workflow_id,
                        'execution_time': t.execution_time,
                        'assigned_volunteer': t.assigned_volunteer,
                        'completed_date': t.completed_date.isoformat() if t.completed_date else None,
                        'cpu_usage': t.cpu_usage,
                        'memory_usage': t.memory_usage
                    } for t in tasks
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

