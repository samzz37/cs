"""
System monitoring module using psutil
"""
import psutil
import json
from datetime import datetime
from typing import Dict, List, TYPE_CHECKING
from dataclasses import dataclass, asdict
import sys
from pathlib import Path

if TYPE_CHECKING:
    from app.models import OnlineUser

@dataclass
class SystemStats:
    """System statistics data class"""
    cpu_usage: float
    memory_usage: float
    memory_total_gb: float
    memory_available_gb: float
    disk_usage: float
    disk_total_gb: float
    disk_free_gb: float
    cpu_count: int
    timestamp: str

@dataclass
class ProcessStats:
    """Process statistics"""
    pid: int
    name: str
    memory_mb: float
    cpu_percent: float
    num_threads: int
    status: str

class MonitoringService:
    """Real-time system monitoring"""
    
    @staticmethod
    def get_system_stats() -> SystemStats:
        """Get current system statistics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return SystemStats(
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            memory_total_gb=memory.total / (1024 ** 3),
            memory_available_gb=memory.available / (1024 ** 3),
            disk_usage=disk.percent,
            disk_total_gb=disk.total / (1024 ** 3),
            disk_free_gb=disk.free / (1024 ** 3),
            cpu_count=psutil.cpu_count(),
            timestamp=datetime.utcnow().isoformat()
        )
    
    @staticmethod
    def get_process_stats(pid: int = None) -> ProcessStats:
        """Get process statistics"""
        import os
        if pid is None:
            pid = os.getpid()
        
        try:
            process = psutil.Process(pid)
            return ProcessStats(
                pid=process.pid,
                name=process.name(),
                memory_mb=process.memory_info().rss / (1024 ** 2),
                cpu_percent=process.cpu_percent(),
                num_threads=process.num_threads(),
                status=process.status()
            )
        except Exception as e:
            return None
    
    @staticmethod
    def get_active_users_count(db) -> int:
        """Get count of active online users"""
        import sys
        from pathlib import Path
        if str(Path(__file__).parent.parent / 'backend') not in sys.path:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
        from app.models import OnlineUser
        from sqlalchemy import func
        return db.query(func.count(OnlineUser.id)).scalar() or 0
    
    @staticmethod
    def check_health() -> Dict:
        """Check overall system health"""
        stats = MonitoringService.get_system_stats()
        
        health = {
            'cpu_ok': stats.cpu_usage < 80,
            'memory_ok': stats.memory_usage < 80,
            'disk_ok': stats.disk_usage < 90,
            'overall_status': 'healthy'
        }
        
        if not all([health['cpu_ok'], health['memory_ok'], health['disk_ok']]):
            health['overall_status'] = 'warning'
        
        return health
    
    @staticmethod
    def get_network_stats() -> Dict:
        """Get network statistics"""
        net_if = psutil.net_if_stats()
        net_io = psutil.net_io_counters()
        
        return {
            'interfaces': dict(net_if),
            'bytes_sent': net_io.bytes_sent,
            'bytes_received': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_received': net_io.packets_recv
        }

class AlertManager:
    """Manage system alerts"""
    
    @staticmethod
    def check_thresholds(stats: SystemStats) -> List[Dict]:
        """Check if thresholds are exceeded"""
        alerts = []
        
        if stats.cpu_usage > 85:
            alerts.append({
                'type': 'high_cpu',
                'message': f'High CPU usage: {stats.cpu_usage}%',
                'severity': 'warning'
            })
        
        if stats.memory_usage > 85:
            alerts.append({
                'type': 'high_memory',
                'message': f'High memory usage: {stats.memory_usage}%',
                'severity': 'warning'
            })
        
        if stats.disk_usage > 90:
            alerts.append({
                'type': 'high_disk',
                'message': f'High disk usage: {stats.disk_usage}%',
                'severity': 'critical'
            })
        
        return alerts
    
    @staticmethod
    def should_send_alert(alert_type: str, last_sent: Dict) -> bool:
        """Check if alert should be sent (throttling)"""
        from datetime import timedelta
        
        if alert_type not in last_sent:
            return True
        
        last_time = last_sent[alert_type]
        if datetime.utcnow() - last_time > timedelta(minutes=5):
            return True
        
        return False

class PerformanceTracker:
    """Track performance metrics over time"""
    
    def __init__(self):
        self.metrics = []
        self.max_records = 1440  # 24 hours of 1-minute samples
    
    def record_stats(self, stats: SystemStats):
        """Record system statistics"""
        self.metrics.append(asdict(stats))
        if len(self.metrics) > self.max_records:
            self.metrics.pop(0)
    
    def get_average_stats(self, minutes: int = 60) -> Dict:
        """Get average stats over past N minutes"""
        if not self.metrics:
            return None
        
        recent_metrics = self.metrics[-minutes:]
        
        avg_cpu = sum(m['cpu_usage'] for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m['memory_usage'] for m in recent_metrics) / len(recent_metrics)
        
        return {
            'avg_cpu': avg_cpu,
            'avg_memory': avg_memory,
            'sample_count': len(recent_metrics)
        }
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict]:
        """Get recent metrics history"""
        return self.metrics[-limit:]
