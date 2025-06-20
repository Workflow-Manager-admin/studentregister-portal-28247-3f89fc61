#!/bin/bash
cd /home/kavia/workspace/code-generation/studentregister-portal-28247-3f89fc61/student_registration_frontend_workspace/student_registration_frontend
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

