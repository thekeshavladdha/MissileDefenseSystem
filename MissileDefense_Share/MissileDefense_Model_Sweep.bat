@echo off
set "JAVA_HOME=C:\Program Files\Java\jdk-17"
set "INSTALL_PATH=C:\Users\satvi\Desktop\VisualSim\VS_AR"
set "CLASS_PATH=%INSTALL_PATH%;%INSTALL_PATH%\com\amity\flexlm\flexlm.jar;%INSTALL_PATH%\com\amity\flexlm\EccpressoAll.jar;%INSTALL_PATH%\com\amity\flexlm\flexlmutil.jar"
set "HERE=%~dp0"
set "HERE=%HERE:~0,-1%"
set "MODEL=%HERE%\MissileDefense_Model.xml"

"%JAVA_HOME%\bin\java" -Dvs.lic=default -Djava.security.policy=%INSTALL_PATH%\bin\policyAll -Djava.security.manager=allow --add-opens java.desktop/sun.font=ALL-UNNAMED -classpath %CLASS_PATH% VisualSim.actor.gui.VisualSimBatchModeSimulator -run 1 -resultpath "%HERE%" -Execution_Time 2.5 -Input_Rate 1.0 -Modelseed seed(1001) -Pk 0.5 -Intercept_Deadline 4.0 -DefenseOutcome.fileName MissileDefense_Outcome_run1.txt "%MODEL%"

"%JAVA_HOME%\bin\java" -Dvs.lic=default -Djava.security.policy=%INSTALL_PATH%\bin\policyAll -Djava.security.manager=allow --add-opens java.desktop/sun.font=ALL-UNNAMED -classpath %CLASS_PATH% VisualSim.actor.gui.VisualSimBatchModeSimulator -run 2 -resultpath "%HERE%" -Execution_Time 2.5 -Input_Rate 1.0 -Modelseed seed(1002) -Pk 0.8 -Intercept_Deadline 4.0 -DefenseOutcome.fileName MissileDefense_Outcome_run2.txt "%MODEL%"

"%JAVA_HOME%\bin\java" -Dvs.lic=default -Djava.security.policy=%INSTALL_PATH%\bin\policyAll -Djava.security.manager=allow --add-opens java.desktop/sun.font=ALL-UNNAMED -classpath %CLASS_PATH% VisualSim.actor.gui.VisualSimBatchModeSimulator -run 3 -resultpath "%HERE%" -Execution_Time 2.5 -Input_Rate 1.0 -Modelseed seed(1003) -Pk 0.95 -Intercept_Deadline 4.0 -DefenseOutcome.fileName MissileDefense_Outcome_run3.txt "%MODEL%"
