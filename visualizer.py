from typing import List, Dict, Any
from ai_trip_planner.engine.models import TripRequest, RouteInfo, RiskTolerance, HotelPreference
from ai_trip_planner.algorithms.search import SearchAlgorithms
import random

class AIEngine:
    def __init__(self, city_network):
        self.city_network = city_network

    def get_recommendations(self, request: TripRequest) -> List[RouteInfo]:
        graph = self.city_network.get_dynamic_data()
        
        # Run multiple algorithms
        results = []
        results.append(SearchAlgorithms.a_star(graph, request.source, request.destination, 'cost'))
        results.append(SearchAlgorithms.ucs(graph, request.source, request.destination, 'time'))
        results.append(SearchAlgorithms.greedy(graph, request.source, request.destination))
        results.append(SearchAlgorithms.bfs(graph, request.source, request.destination))

        recommendations = []
        for res in results:
            if not res: continue
            
            # AI Utility Calculation
            utility = self._calculate_utility(res, request)
            explanation = self._generate_explanation(res, request, utility)
            
            route = RouteInfo(
                path=res['path'],
                total_distance=res['total_distance'],
                total_cost=res['total_cost'],
                total_time=res['total_time'],
                avg_traffic=res['avg_traffic'],
                max_risk=res['max_risk'],
                algorithm=res['algorithm'],
                explored_nodes=res['explored_nodes'],
                execution_time=res['execution_time'],
                explanation=explanation
            )
            recommendations.append(route)
            
        # Sort by utility (simplified here as budget/risk filtering)
        filtered = [r for r in recommendations if r.total_cost <= request.budget * 1.2]
        return sorted(filtered, key=lambda x: x.total_cost)

    def _calculate_utility(self, res, request):
        # Higher is better
        score = 1000
        # Penalty for exceeding budget
        if res['total_cost'] > request.budget:
            score -= (res['total_cost'] - request.budget) * 2
        # Penalty for high risk if tolerance is low
        if request.risk_tolerance == RiskTolerance.LOW:
            score -= res['max_risk'] * 500
        # Penalty for time
        score -= res['total_time'] * 10
        return score

    def _generate_explanation(self, res, request, utility):
        reasons = []
        if res['total_cost'] <= request.budget:
            reasons.append("Fits well within your budget.")
        else:
            reasons.append("Slightly over budget but offers faster transit.")
            
        if res['max_risk'] < 0.3:
            reasons.append("Low weather risk detected on this route.")
        elif request.risk_tolerance == RiskTolerance.HIGH:
            reasons.append("Higher risk route, but optimized for cost/time.")
            
        if res['avg_traffic'] < 0.4:
            reasons.append("Expect smooth traffic conditions.")
            
        return " ".join(reasons)

    def get_hotel_recommendation(self, city: str, pref: HotelPreference):
        hotels = {
            HotelPreference.BUDGET: ["Zostel", "OYO Townhouse", "Ibis Budget"],
            HotelPreference.STANDARD: ["Novotel", "Lemon Tree", "Holiday Inn"],
            HotelPreference.LUXURY: ["Taj Palace", "The Oberoi", "ITC Grand"]
        }
        name = random.choice(hotels[pref])
        price = random.randint(2000, 5000) if pref == HotelPreference.BUDGET else \
                random.randint(5000, 12000) if pref == HotelPreference.STANDARD else \
                random.randint(15000, 45000)
        return {"name": f"{name} {city}", "price_per_night": price, "rating": round(random.uniform(3.5, 5.0), 1)}

    def analyze_risk(self, route: RouteInfo):
        risk_level = "Low"
        if route.max_risk > 0.7: risk_level = "Critical"
        elif route.max_risk > 0.4: risk_level = "Moderate"
        
        return {
            "risk_level": risk_level,
            "weather_forecast": "Unstable" if route.max_risk > 0.5 else "Clear",
            "traffic_impact": f"{int(route.avg_traffic * 100)}% delay expected"
        }
