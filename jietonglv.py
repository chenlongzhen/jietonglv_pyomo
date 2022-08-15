from __future__ import division
import pyomo.environ as pyo

model = pyo.AbstractModel()

model.x = pyo.Param(within=pyo.NonNegativeIntegers)
model.y = pyo.Param(within=pyo.NonNegativeIntegers)

model.i = pyo.RangeSet(1, model.x)
model.j = pyo.RangeSet(1, model.y)

model.A = pyo.Param(model.i, model.i)
model.C = pyo.Param(model.i)

# the next line declares a variable indexed by the set J
model.B = pyo.Var(model.i, model.j, domain=pyo.NonNegativeReals)


def obj_expression(m):
    obj =  sum(sum(m.A[i, j] * m.B[i, j] for j in m.y) * m.C[i] for i in m.x) \
           / sum(m.C[i] for i in m.x)
    return -obj


model.OBJ = pyo.Objective(rule=obj_expression)


def constraint_rule_1(m, i):
    # return the expression for the constraint for i
    return sum(m.B[i, j] for j in m.J) == 1


def constraint_rule_2(m, j):
    # return the expression for the constraint for i
    return sum(m.B[i, j] * m.C[i] for i in m.j) == 1


def constraint_rule_3(m, i, j):
    # return the expression for the constraint for i
    return m.B[i, j] <= 1


# the next line creates one constraint for each member of the set model.I
model.AxbConstraint1 = pyo.Constraint(model.i, rule=constraint_rule_1)
model.AxbConstraint2 = pyo.Constraint(model.j, rule=constraint_rule_2)
model.AxbConstraint3 = pyo.Constraint(model.i, model.j, rule=constraint_rule_3)
