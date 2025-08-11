-- Users
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password TEXT,
  role VARCHAR(20) NOT NULL CHECK (role IN ('admin','member')),
  status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive')),
  join_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Workout Plans
CREATE TABLE IF NOT EXISTS workout_plans (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan_name VARCHAR(100) NOT NULL,
  plan_details TEXT NOT NULL,
  duration_weeks INT NOT NULL,
  created_by INT NOT NULL REFERENCES users(id)
);

-- Meal Plans
CREATE TABLE IF NOT EXISTS meal_plans (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  meal_name VARCHAR(100) NOT NULL,
  meal_details TEXT NOT NULL,
  goal VARCHAR(50) NOT NULL,
  created_by INT NOT NULL REFERENCES users(id)
);

-- Progress Logs
CREATE TABLE IF NOT EXISTS progress_logs (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  weight DECIMAL(5,2) NOT NULL,
  body_fat_percentage DECIMAL(5,2) NOT NULL,
  bmi DECIMAL(5,2) NOT NULL,
  log_date TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_progress_user_date ON progress_logs(user_id, log_date DESC);

-- Payment Reminders (extended with amount and status)
CREATE TABLE IF NOT EXISTS payment_reminders (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  due_date DATE NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  upi_link TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','sent','paid'))
);
CREATE INDEX IF NOT EXISTS idx_payment_user_status ON payment_reminders(user_id, status);