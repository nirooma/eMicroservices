[
   {
      "name":"leonardo",
      "image":"nirooma/leonardo:latest",
      "cpu":10,
      "command":[
         "daphne",
         "--bind",
         "0.0.0.0",
         "--port",
         "8002",
         "core.asgi:application"
      ],
      "memory":512,
      "links":[
         "leonardo-db",
         "rabbitmq"
      ],
      "essential":true,
      "environment":[
         {
            "name":"SQL_ENGINE",
            "value":"django.db.backends.postgresql"
         },
         {
            "name":"SQL_DATABASE",
            "value":"fastapi"
         },
         {
            "name":"SQL_USER",
            "value":"postgres"
         },
         {
            "name":"SQL_PASSWORD",
            "value":"postgres"
         },
         {
            "name":"SQL_HOST",
            "value":"leonardo-db"
         },
         {
            "name":"SQL_PORT",
            "value":"5432"
         }
      ],
      "portMappings":[
         {
            "containerPort":8002
         }
      ],
      "mountPoints":[
         {
            "containerPath":"/opt/leonardo/staticfiles",
            "sourceVolume":"staticfiles"
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream_leonardo}"
         }
      }
   },
   {
      "name":"leonardo-db",
      "image":"postgres:13.4-alpine",
      "cpu":10,
      "memory":256,
      "essential":true,
      "environment":[
         {
            "name":"POSTGRES_DB",
            "value":"fastapi"
         },
         {
            "name":"POSTGRES_USER",
            "value":"postgres"
         },
         {
            "name":"POSTGRES_PASSWORD",
            "value":"postgres"
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream_leonardo}"
         }
      }
   },
   {
      "name":"rabbitmq",
      "image":"rabbitmq:3.9.4-management",
      "cpu":10,
      "memory":256,
      "essential":true,
      "environment":[],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream_rabbitmq}"
         }
      }
   },
   {
      "name":"splinter",
      "image":"nirooma/splinter:latest",
      "cpu":10,
      "command":[
         "yarn",
         "start"
      ],
      "memory":128,
      "essential":true,
      "environment":[

      ],
      "portMappings":[
         {
            "containerPort":3000
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream_splinter}"
         }
      }
   },
   {
      "name":"nginx",
      "image":"nirooma/nginx:latest",
      "cpu":10,
      "memory":128,
      "links":[
         "splinter",
         "leonardo",
         "rabbitmq"
      ],
      "essential":true,
      "environment":[],
      "portMappings":[
         {
            "containerPort":80
         },
         {
            "containerPort":15672
         }
      ],
      "mountPoints":[
         {
            "containerPath":"/opt/leonardo/staticfiles",
            "sourceVolume":"staticfiles"
         }
      ],
      "logConfiguration":{
         "logDriver":"awslogs",
         "options":{
            "awslogs-group":"${aws_cloudwatch_log_group}",
            "awslogs-region":"eu-central-1",
            "awslogs-stream-prefix":"${aws_cloudwatch_log_stream_nginx}"
         }
      }
   }
]