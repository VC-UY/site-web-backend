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

