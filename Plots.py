import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

df = textfile
y = df['Y-Axis'].values
X_lin = df['X-Axis'].values[:, np.newaxis]

rg = LinearRegression()

# Create quadratic features
quadratic = PolynomialFeatures(degree=2)
cubic = PolynomialFeatures(degree=3)
X_quad = quadratic.fit_transform(X_lin)
X_cubic = cubic.fit_transform(X_lin)

# Fit features
lin_rg = LinearRegression()
lin_rg.fit(X_lin, y)
linear_r2 = r2_score(y, lin_rg.predict(X_lin))

quad_rg = LinearRegression()
quad_rg.fit(X_quad, y)
quadratic_r2 = r2_score(y, quad_rg.predict(X_quad))

cubic_rg = LinearRegression()
cubic_rg.fit(X_cubic, y)
cubic_r2 = r2_score(y, cubic_rg.predict(X_cubic))

# Plot results
X_range = np.arange(X_lin.min(), X_lin.max(), 1)[:, np.newaxis]
y_lin_pred = lin_rg.predict(X_range)
y_quad_pred = quad_rg.predict(quadratic.fit_transform(X_range))
y_cubic_pred = cubic_rg.predict(cubic.fit_transform(X_range))

plt.scatter(X_lin, y, label='Training points', color='lightgray')

plt.plot(X_range, y_lin_pred, label='Linear (d=1), $R^2=%.2f$' % linear_r2, color='blue', lw=2, linestyle=':')

plt.plot(X_range, y_quad_pred, label='Quadratic (d=2), $R^2=%.2f$' % quadratic_r2, color='red', lw=2, linestyle='-')

plt.plot(X_range, y_cubic_pred, label='Cubic (d=3), $R^2=%.2f$' % cubic_r2, color='green', lw=2, linestyle='--')

plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.legend(loc='upper right')
plt.title("Happy Chart")

plt.tight_layout()
plt.show()