-- Create role gx_user.
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM pg_roles
    WHERE rolname = 'gx_user'
) THEN CREATE USER gx_user WITH ENCRYPTED PASSWORD 'gx_user_password';
END IF;
END $$;

-- Create demo database and grant permissions to gx_user.
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'demo'
) THEN CREATE DATABASE gx;
GRANT ALL PRIVILEGES ON DATABASE demo TO gx_user;
GRANT ALL ON SCHEMA public TO gx_user;
END IF;
END $$;