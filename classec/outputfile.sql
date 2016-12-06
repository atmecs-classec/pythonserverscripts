-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cloud_assessment
-- ------------------------------------------------------
-- Server version	5.5.53-0ubuntu0.14.04.1
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'cloud_assessment'
--
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`100.100.100.1` PROCEDURE `sp_appcost`()
BEGIN
CREATE TEMPORARY TABLE IF NOT EXISTS appinfo
(
Param_name varchar(100) not null,
Param_value integer not null
);

INSERT into appinfo (Param_name, Param_value)
		Select "EC2 Instances", count(*) from cloud_assessment.vw_ec2withcost WHERE `ec2_name` LIKE '%my%store%news%' ;

INSERT into appinfo (Param_name, Param_value)
		Select "EBS Volumes", count(*) from cloud_assessment.ebs_static WHERE `ebs_service` LIKE  '%my%store%news%';
        
INSERT into appinfo (Param_name, Param_value)
		Select "RDS Instances", count(*) from cloud_assessment.rds_static_instance WHERE `DBInstanceIdentifier` LIKE  '%store%news%';

INSERT into appinfo (Param_name, Param_value)
		Select "ELB Instances", count(*) FROM  cloud_assessment.elb_static WHERE  `LoadBalancerName` LIKE  '%my%store%news%';
                
Select * from appinfo;

DROP temporary table appinfo;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`100.100.100.1` PROCEDURE `sp_dashboard`()
BEGIN
CREATE TEMPORARY TABLE IF NOT EXISTS dashboardinfo
(
Param_name varchar(100) not null,
Param_value integer not null
);

INSERT into dashboardinfo (Param_name, Param_value)
		Select "Stopped Instances", count(*) from cloud_assessment.vw_ec2withcost where ec2_state='stopped';

INSERT into dashboardinfo (Param_name, Param_value)
		Select "Production Instances", count(*) from cloud_assessment.vw_ec2withcost where ec2_env='production';
        
INSERT into dashboardinfo (Param_name, Param_value)
		Select "EC2 Total Cost", sum(cost) from cloud_assessment.vw_ec2withcost;

INSERT into dashboardinfo (Param_name, Param_value)
		Select "Unattached Volumes", count(ebs_volumeid) from cloud_assessment.ebs_static where ebs_state='available';
                
Select * from dashboardinfo;

DROP temporary table dashboardinfo;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`100.100.100.1` PROCEDURE `sp_ec2cpuutilcost`()
BEGIN
Declare uavg double;
Declare umax double;
Select service_threshold into @uavg from user_config where service_param='avg_cpu_util';
Select service_threshold into @umax from user_config where service_param='max_cpu_util';
select a.ec_id, a.ec2_name, a.ec2_domain, a.ec2_state, a.ec2_env, a.ec2_type, a.Ec2_platform, a.cost from cloud_assessment.vw_ec2withcost a, cloud_assessment.ec2_dynamic b where ec2_cpu_util_avg < @uavg and ec2_cpu_util_max < @umax and a.ec_id = b.inst_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`100.100.100.1` PROCEDURE `sp_ec2withcost`()
BEGIN
(select a.ec_id,a.ec2_name,ec2_domain,ec2_state,a.ec2_env,a.ec2_type,a.Ec2_platform, b.windows_re as "cost" from cloud_assessment.ec2_static a, cloud_assessment.ec2_cost b 
where a.ec2_type=b.type and substring(ec2_region, 1, char_length(ec2_region)-1)=b.Region and a.Ec2_platform="windows")
UNION
(select a.ec_id,a.ec2_name,ec2_domain,ec2_state,a.ec2_env,a.ec2_type,a.Ec2_platform, b.linux_re as "cost" from cloud_assessment.ec2_static a, cloud_assessment.ec2_cost b 
where a.ec2_type=b.type and substring(ec2_region, 1, char_length(ec2_region)-1)=b.Region and a.Ec2_platform="");
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`100.100.100.1` PROCEDURE `sp_topdashboard`()
BEGIN
CREATE TEMPORARY TABLE IF NOT EXISTS topdashboardinfo
(
Param_name varchar(100) not null,
Param_value integer not null
);

INSERT into topdashboardinfo (Param_name, Param_value)
		Select "EC2 Instances", count(*) from cloud_assessment.vw_ec2withcost;

INSERT into topdashboardinfo (Param_name, Param_value)
		Select "EBS Volumes", count(*) from cloud_assessment.ebs_static;
        
INSERT into topdashboardinfo (Param_name, Param_value)
		Select "RDS Instances", count(*) from cloud_assessment.rds_static_instance;

INSERT into topdashboardinfo (Param_name, Param_value)
		Select "EMR Instances", count(*) from cloud_assessment.emr_static;
                
Select * from topdashboardinfo;

DROP temporary table topdashboardinfo;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-06 11:14:33
