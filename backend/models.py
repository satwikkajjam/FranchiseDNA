"""
Database Models for FranchiseDNA.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PopulationData(db.Model):
    __tablename__ = 'population_data'

    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(200), nullable=False, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    population = db.Column(db.BigInteger)
    working_population = db.Column(db.BigInteger)
    households = db.Column(db.BigInteger)
    literate_population = db.Column(db.BigInteger)
    literacy_rate = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'area': self.area,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'population': self.population,
            'working_population': self.working_population,
            'households': self.households,
            'literate_population': self.literate_population,
            'literacy_rate': self.literacy_rate,
        }


class FranchiseType(db.Model):
    __tablename__ = 'franchise_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    area_sqft_min = db.Column(db.Integer)
    area_sqft_max = db.Column(db.Integer)
    setup_cost = db.Column(db.Float, nullable=False)
    investment = db.Column(db.Float)
    avg_daily_revenue = db.Column(db.Float)
    avg_customer_spend = db.Column(db.Float, nullable=False)
    employees_required = db.Column(db.Integer, nullable=False)
    monthly_operating_cost = db.Column(db.Float, nullable=False)
    profit_margin = db.Column(db.Float, nullable=False)  # as decimal 0-1
    min_population = db.Column(db.Integer, default=10000)
    target_demographic = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'area_sqft': f"{self.area_sqft_min}-{self.area_sqft_max}" if self.area_sqft_min else None,
            'area_sqft_min': self.area_sqft_min,
            'area_sqft_max': self.area_sqft_max,
            'setup_cost': self.setup_cost,
            'investment': self.investment,
            'avg_daily_revenue': self.avg_daily_revenue,
            'avg_customer_spend': self.avg_customer_spend,
            'employees_required': self.employees_required,
            'monthly_operating_cost': self.monthly_operating_cost,
            'profit_margin': self.profit_margin,
            'min_population': self.min_population,
            'target_demographic': self.target_demographic,
        }


class AnalysisReport(db.Model):
    __tablename__ = 'analysis_reports'

    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius_km = db.Column(db.Float)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchise_types.id'))
    total_population = db.Column(db.BigInteger)
    working_population = db.Column(db.BigInteger)
    total_households = db.Column(db.BigInteger)
    competitor_count = db.Column(db.Integer)
    estimated_daily_customers = db.Column(db.Integer)
    estimated_daily_revenue = db.Column(db.Float)
    estimated_yearly_revenue = db.Column(db.Float)
    estimated_yearly_profit = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    risk_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    franchise = db.relationship('FranchiseType', backref='reports')

    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius_km': self.radius_km,
            'franchise': self.franchise.to_dict() if self.franchise else None,
            'total_population': self.total_population,
            'working_population': self.working_population,
            'total_households': self.total_households,
            'competitor_count': self.competitor_count,
            'estimated_daily_customers': self.estimated_daily_customers,
            'estimated_daily_revenue': self.estimated_daily_revenue,
            'estimated_yearly_revenue': self.estimated_yearly_revenue,
            'estimated_yearly_profit': self.estimated_yearly_profit,
            'risk_level': self.risk_level,
            'risk_score': self.risk_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
