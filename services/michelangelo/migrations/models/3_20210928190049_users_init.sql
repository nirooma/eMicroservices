-- upgrade --
ALTER TABLE "user" ADD "first_name" VARCHAR(255)   DEFAULT '';
ALTER TABLE "user" ADD "last_name" VARCHAR(255)   DEFAULT '';
-- downgrade --
ALTER TABLE "user" DROP COLUMN "first_name";
ALTER TABLE "user" DROP COLUMN "last_name";
