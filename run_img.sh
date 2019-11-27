docker run --rm --name gateway_test \
-v `pwd`/comp_dispatch:/comp_dispatch \
-v `pwd`/model_connect_setting:/model_connect_setting \
-v `pwd`/models_result_config:/models_result_config \
-p $EXPOSE_PORT:5000 \
--expose=$EXPOSE_PORT \
$GATEWAY_IMG_TAG
