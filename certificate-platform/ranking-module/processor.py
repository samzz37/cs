"""
Ranking Module - Student Merit Ranking System
"""

class RankingProcessor:
    """Process and manage student rankings"""
    
    def __init__(self, db):
        self.db = db
    
    def calculate_rankings(self, event: str, academic_year: str) -> list:
        """Calculate rankings for an event"""
        from ..backend.app import models
        
        rankings = self.db.query(models.Ranking).filter(
            models.Ranking.event == event,
            models.Ranking.academic_year == academic_year
        ).order_by(models.Ranking.marks.desc()).all()
        
        # Assign positions
        for position, ranking in enumerate(rankings, 1):
            ranking.rank_position = position
        
        self.db.commit()
        return rankings
    
    def export_rankings(self, event: str, academic_year: str, format: str) -> str:
        """Export rankings in various formats"""
        from ..exports.exporter import RankingExporter
        
        rankings = self.calculate_rankings(event, academic_year)
        exporter = RankingExporter([r.__dict__ for r in rankings])
        
        if format == 'pdf':
            return exporter.export_pdf(f'rankings_{event}_{academic_year}.pdf')
        elif format == 'excel':
            return exporter.export_excel(f'rankings_{event}_{academic_year}.xlsx')
        elif format == 'csv':
            return exporter.export_csv(f'rankings_{event}_{academic_year}.csv')
        elif format == 'word':
            return exporter.export_word(f'rankings_{event}_{academic_year}.docx')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_top_performers(self, event: str, academic_year: str, limit: int = 10) -> list:
        """Get top performers"""
        from ..backend.app import models
        
        return self.db.query(models.Ranking).filter(
            models.Ranking.event == event,
            models.Ranking.academic_year == academic_year
        ).order_by(models.Ranking.marks.desc()).limit(limit).all()
    
    def get_department_rankings(self, department: str, limit: int = 100) -> list:
        """Get rankings by department"""
        from ..backend.app import models
        
        return self.db.query(models.Ranking).filter(
            models.Ranking.department == department
        ).order_by(models.Ranking.marks.desc()).limit(limit).all()
