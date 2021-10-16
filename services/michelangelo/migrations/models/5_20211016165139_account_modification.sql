-- upgrade --
ALTER TABLE "account" ADD "account_token" VARCHAR(255);
ALTER TABLE "account" ADD "two_factor_auth" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "account" DROP COLUMN "account_token";
ALTER TABLE "account" DROP COLUMN "two_factor_auth";
