-- upgrade --
ALTER TABLE "user" DROP COLUMN "is_staff";
-- downgrade --
ALTER TABLE "user" ADD "is_staff" BOOL NOT NULL  DEFAULT False;
