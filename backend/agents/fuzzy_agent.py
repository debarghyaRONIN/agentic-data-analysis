import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class FuzzyPredictionAgent:
    """
    Predicts ORDER FLOW based on rating and volatility
    """

    def __init__(self):
        self._build_system()

    def _build_system(self):


        # INPUTS (Antecedents)

        self.rating = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'rating')
        self.volatility = ctrl.Antecedent(np.arange(0, 101, 1), 'volatility')

 
        # OUTPUT (Consequent)

        self.order_flow = ctrl.Consequent(np.arange(0, 301, 1), 'order_flow')

        # Membership functions

        self.rating['low'] = fuzz.trimf(self.rating.universe, [0, 0, 3])
        self.rating['medium'] = fuzz.trimf(self.rating.universe, [2.5, 3.5, 4.5])
        self.rating['high'] = fuzz.trimf(self.rating.universe, [4, 5, 5])

        self.volatility['low'] = fuzz.trimf(self.volatility.universe, [0, 0, 30])
        self.volatility['medium'] = fuzz.trimf(self.volatility.universe, [20, 40, 60])
        self.volatility['high'] = fuzz.trimf(self.volatility.universe, [50, 100, 100])

        self.order_flow['low'] = fuzz.trimf(self.order_flow.universe, [0, 0, 120])
        self.order_flow['medium'] = fuzz.trimf(self.order_flow.universe, [100, 150, 200])
        self.order_flow['high'] = fuzz.trimf(self.order_flow.universe, [180, 300, 300])


        # RULE BASE

        rules = [
            ctrl.Rule(self.rating['high'] & self.volatility['low'], self.order_flow['high']),
            ctrl.Rule(self.rating['medium'] & self.volatility['medium'], self.order_flow['medium']),
            ctrl.Rule(self.rating['low'] | self.volatility['high'], self.order_flow['low']),
        ]

        system = ctrl.ControlSystem(rules)
        self.simulator = ctrl.ControlSystemSimulation(system)


    # PREDICTION

    def predict(self, rating: float, volatility: float):
        self.simulator.input['rating'] = rating
        self.simulator.input['volatility'] = volatility
        self.simulator.compute()

        order_flow_value = self.simulator.output['order_flow']

        level = (
            "HIGH" if order_flow_value > 180 else
            "MEDIUM" if order_flow_value > 120 else
            "LOW"
        )

        output = {
            "predicted_order_flow": round(order_flow_value, 2),
            "order_flow_level": level
        }

        print("🔮 Fuzzy Agent Output:", output)
        return output


    #  NEW: EXPORT MEMBERSHIP FUNCTIONS

    def get_membership_charts(self):
        """
        Returns membership functions for frontend visualization
        """

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
            "volatility": extract(self.volatility),
            "order_flow": extract(self.order_flow)
        }
