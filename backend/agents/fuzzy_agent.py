import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyPredictionAgent:

    def __init__(self):
        self._build_system()

    def _build_system(self):

        # INPUTS
        self.rating = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'rating')
        self.order_hour = ctrl.Antecedent(np.arange(0, 24, 1), 'order_hour')
        self.volatility = ctrl.Antecedent(np.arange(0, 101, 1), 'volatility')

        # OUTPUT
        self.order_flow = ctrl.Consequent(np.arange(0, 301, 1), 'order_flow')

        # RATING MEMBERSHIP
        self.rating['low'] = fuzz.trimf(self.rating.universe, [0, 0, 3])
        self.rating['medium'] = fuzz.trimf(self.rating.universe, [2.5, 3.5, 4.5])
        self.rating['high'] = fuzz.trimf(self.rating.universe, [4, 5, 5])

        # TIME MEMBERSHIP
        self.order_hour['morning'] = fuzz.trimf(self.order_hour.universe, [0, 6, 12])
        self.order_hour['afternoon'] = fuzz.trimf(self.order_hour.universe, [11, 14, 17])
        self.order_hour['evening'] = fuzz.trimf(self.order_hour.universe, [16, 20, 23])

        # VOLATILITY MEMBERSHIP
        self.volatility['low'] = fuzz.trimf(self.volatility.universe, [0, 0, 30])
        self.volatility['medium'] = fuzz.trimf(self.volatility.universe, [20, 50, 70])
        self.volatility['high'] = fuzz.trimf(self.volatility.universe, [60, 100, 100])

        # ORDER FLOW MEMBERSHIP
        self.order_flow['low'] = fuzz.trimf(self.order_flow.universe, [0, 0, 120])
        self.order_flow['medium'] = fuzz.trimf(self.order_flow.universe, [100, 150, 200])
        self.order_flow['high'] = fuzz.trimf(self.order_flow.universe, [180, 300, 300])

        # RULE BASE

        rules = [

            # Evening peak demand
            ctrl.Rule(self.rating['high'] & self.order_hour['evening'] & self.volatility['low'], self.order_flow['high']),

            # Afternoon stable demand
            ctrl.Rule(self.rating['medium'] & self.order_hour['afternoon'] & self.volatility['medium'], self.order_flow['medium']),

            # Morning generally low
            ctrl.Rule(self.order_hour['morning'], self.order_flow['low']),

            # High volatility reduces flow
            ctrl.Rule(self.volatility['high'], self.order_flow['low']),

            # Safety rule
            ctrl.Rule(self.rating['low'], self.order_flow['low'])
        ]

        system = ctrl.ControlSystem(rules)
        self.simulator = ctrl.ControlSystemSimulation(system)

    # PREDICTION
    def predict(self, rating, order_hour, volatility):

        self.simulator.input['rating'] = rating
        self.simulator.input['order_hour'] = order_hour
        self.simulator.input['volatility'] = volatility

        self.simulator.compute()

        order_flow_value = self.simulator.output['order_flow']

        level = (
            "HIGH" if order_flow_value > 180 else
            "MEDIUM" if order_flow_value > 120 else
            "LOW"
        )

        return {
            "predicted_order_flow": round(order_flow_value, 2),
            "order_flow_level": level
        }

    # EXPORT MEMBERSHIP CHARTS
    def get_membership_charts(self):

        def extract(variable):
            return {
                "x": variable.universe.tolist(),
                **{
                    name: term.mf.tolist()
                    for name, term in variable.terms.items()
                }
            }

        return {
            "rating": extract(self.rating),
            "order_hour": extract(self.order_hour),
            "volatility": extract(self.volatility),
            "order_flow": extract(self.order_flow)
        }
