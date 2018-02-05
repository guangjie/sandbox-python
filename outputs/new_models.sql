SET @HertzId = 37;
SET @CountryIdChina = 44;
SET @CountryIdMalaysien = 128;
SET @CountryIdTaiwan = 207;
SET @CountryIdMyanmar = 145;
SET @IdentCode = 'ddd'; 
SET @ModelName = 'aaa'; 

INSERT INTO `mdx_kfz_models` (`herst`, `name`, `ident_code`) 
SELECT * FROM (SELECT @HertzId, @ModelName, @IdentCode) AS tmp 
WHERE NOT EXISTS ( 
	 SELECT `ident_code` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode 
) LIMIT 1; 

SET @ModelId = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode); 

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdChina) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdChina
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMalaysien) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMalaysien
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdTaiwan) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdTaiwan
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMyanmar) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMyanmar
) LIMIT 1;

SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = 'mercedesbenzglcklasse');

INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) 
SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp 
WHERE NOT EXISTS ( 
	SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent 
) LIMIT 1; 

SET @IdentCode = 'fff'; 
SET @ModelName = 'bbb'; 

INSERT INTO `mdx_kfz_models` (`herst`, `name`, `ident_code`) 
SELECT * FROM (SELECT @HertzId, @ModelName, @IdentCode) AS tmp 
WHERE NOT EXISTS ( 
	 SELECT `ident_code` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode 
) LIMIT 1; 

SET @ModelId = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode); 

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdChina) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdChina
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMalaysien) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMalaysien
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdTaiwan) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdTaiwan
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMyanmar) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMyanmar
) LIMIT 1;

SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = 'mercedesbenzglcklasse');

INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) 
SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp 
WHERE NOT EXISTS ( 
	SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent 
) LIMIT 1; 

SET @IdentCode = 'eee'; 
SET @ModelName = 'ccc'; 

INSERT INTO `mdx_kfz_models` (`herst`, `name`, `ident_code`) 
SELECT * FROM (SELECT @HertzId, @ModelName, @IdentCode) AS tmp 
WHERE NOT EXISTS ( 
	 SELECT `ident_code` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode 
) LIMIT 1; 

SET @ModelId = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = @IdentCode); 

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdChina) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdChina
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMalaysien) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMalaysien
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdTaiwan) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdTaiwan
) LIMIT 1;

INSERT INTO `mdx_kfz_model_countries` (`id`, `countryId`) 
SELECT * FROM (SELECT @ModelId, @CountryIdMyanmar) AS tmp 
WHERE NOT EXISTS (
	SELECT `id` FROM `mdx_kfz_model_countries` WHERE `id` = @ModelId AND `countryId` = @CountryIdMyanmar
) LIMIT 1;

SET @ModelParent = (SELECT `id` FROM `mdx_kfz_models` WHERE `ident_code` = 'mercedesbenzglcklasse');

INSERT INTO `mdx_kfz_model_parent` (`modelId`, `parentModelId`) 
SELECT * FROM (SELECT @ModelId, @ModelParent) AS tmp 
WHERE NOT EXISTS ( 
	SELECT `modelId` FROM `mdx_kfz_model_parent` WHERE `modelId` = @ModelId AND `parentModelId` = @ModelParent 
) LIMIT 1; 

