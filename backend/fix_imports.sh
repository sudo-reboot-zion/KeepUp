#!/bin/bash
# Comprehensive import fix script

echo "Fixing all broken imports from cleanup..."

# 1. Fix models/__init__.py - remove social imports
sed -i '/from \.social import/d' /home/gee/bread/AI/KeepUp/backend/models/__init__.py

# 2. Comment out task_management and occupation imports in workflows/daily_check_workflow.py
sed -i 's/^from agents\.task_management/# from agents.task_management/' /home/gee/bread/AI/KeepUp/backend/workflows/daily_check_workflow.py
sed -i 's/^from agents\.occupation/# from agents.occupation/' /home/gee/bread/AI/KeepUp/backend/workflows/daily_check_workflow.py

# 3. Comment out task_management imports in services/adaptive_recommendation_service.py
sed -i 's/^from agents\.task_management/# from agents.task_management/' /home/gee/bread/AI/KeepUp/backend/services/adaptive_recommendation_service.py

# 4. Comment out opik imports
sed -i 's/^from backend\.services\.opik_service/# from backend.services.opik_service/' /home/gee/bread/AI/KeepUp/backend/services/weekly_analysis_job.py
sed -i 's/^from evaluation\.opik_logger/# from evaluation.opik_logger/' /home/gee/bread/AI/KeepUp/backend/services/adaptive_recommendation_service.py

# 5. Comment out social model imports in milestone_service.py
sed -i 's/^from models\.social/# from models.social/' /home/gee/bread/AI/KeepUp/backend/services/milestone_service.py
sed -i 's/^from ws\.connection_manager/# from ws.connection_manager/' /home/gee/bread/AI/KeepUp/backend/services/milestone_service.py

echo "Import fixes complete!"
