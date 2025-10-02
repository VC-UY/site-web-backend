from src.models.user import db
from datetime import datetime

class SystemMetrics(db.Model):
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_volunteers = db.Column(db.Integer, default=0)
    active_volunteers = db.Column(db.Integer, default=0)
    total_tasks = db.Column(db.Integer, default=0)
    completed_tasks = db.Column(db.Integer, default=0)
    pending_tasks = db.Column(db.Integer, default=0)
    cpu_usage = db.Column(db.Float, default=0.0)
    memory_usage = db.Column(db.Float, default=0.0)
    network_throughput = db.Column(db.Float, default=0.0)
    cost_savings = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'total_volunteers': self.total_volunteers,
            'active_volunteers': self.active_volunteers,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'pending_tasks': self.pending_tasks,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'network_throughput': self.network_throughput,
            'cost_savings': self.cost_savings
        }

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='inactive')  # active, inactive, busy
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    tasks_completed = db.Column(db.Integer, default=0)
    total_computation_time = db.Column(db.Float, default=0.0)  # en heures
    cpu_cores = db.Column(db.Integer, default=1)
    memory_gb = db.Column(db.Float, default=1.0)
    performance_score = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'volunteer_id': self.volunteer_id,
            'name': self.name,
            'status': self.status,
            'joined_date': self.joined_date.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'tasks_completed': self.tasks_completed,
            'total_computation_time': self.total_computation_time,
            'cpu_cores': self.cpu_cores,
            'memory_gb': self.memory_gb,
            'performance_score': self.performance_score
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(100), unique=True, nullable=False)
    workflow_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    assigned_volunteer = db.Column(db.String(100), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    started_date = db.Column(db.DateTime, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)
    execution_time = db.Column(db.Float, default=0.0)  # en secondes
    cpu_usage = db.Column(db.Float, default=0.0)
    memory_usage = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'workflow_id': self.workflow_id,
            'status': self.status,
            'assigned_volunteer': self.assigned_volunteer,
            'created_date': self.created_date.isoformat(),
            'started_date': self.started_date.isoformat() if self.started_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'execution_time': self.execution_time,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage
        }

class PerformanceHistory(db.Model):
    __tablename__ = 'performance_history'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    volunteer_id = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.String(100), nullable=False)
    execution_time = db.Column(db.Float, nullable=False)
    cpu_usage = db.Column(db.Float, default=0.0)
    memory_usage = db.Column(db.Float, default=0.0)
    success = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'volunteer_id': self.volunteer_id,
            'task_id': self.task_id,
            'execution_time': self.execution_time,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'success': self.success
        }

