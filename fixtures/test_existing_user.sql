PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
INSERT INTO "auth_user" VALUES(2,'existing','Existing','User','existing@xample.com','sha1$685c4$3a2362412a7710c7a339ecd7130f1a626fb63084',1,1,1,'2012-02-22 20:43:10','2012-02-22 20:43:10');
COMMIT;
