CREATE TABLE IF NOT EXISTS "event_type" (
  "guild_id" BIGINT NOT NULL,
  "type_id" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1000 MINVALUE 1 MAXVALUE 9999 CACHE 1 );,
  "title" TEXT NOT NULL,
  "description" TEXT,
  "role_id" BIGINT NOT NULL,
  "role_color" TEXT,
  "created_at" TIMESTAMP NOT NULL,
  "started_at" TIMESTAMP,
  "disabled_at" TIMESTAMP,
  "enabled" BOOLEAN,
  "message_id" BIGINT,
  "channel_id" BIGINT,
  "emoji" TEXT
);
CREATE TABLE IF NOT EXISTS "event" (
  "guild_id" BIGINT NOT NULL,
  "event_id" BIGINT NOT NULL NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 10000 MINVALUE 1 MAXVALUE 99999 CACHE 1 );,
  "type_id" BIGINT NOT NULL,
  "title" TEXT NOT NULL,
  "details" TEXT,
  "role_id" BIGINT NOT NULL,
  "role_color" TEXT,
  "created_at" TIMESTAMP NOT NULL,
  "started_at" TIMESTAMP,
  "disabled_at" TIMESTAMP,
  "enabled" BOOLEAN,
  "message_id" BIGINT,
  "channel_id" BIGINT,
  "emoji" TEXT
);
CREATE TABLE IF NOT EXISTS "guild" (
  "guild_id" BIGINT NOT NULL,
  "moderator_role_id" BIGINT,
  "title" TEXT NOT NULL
);