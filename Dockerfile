FROM locustio/locust

# Set environment variables for permissions
ENV LOG_DIR=/mnt/logs
ENV LOG_FILE=$LOG_DIR/locust_logs.log
# Create the logs directory and set permissions
USER root
RUN mkdir -p $LOG_DIR && \
    touch $LOG_FILE && \
    chmod -R 777 $LOG_DIR
# Switch back to non-root user
USER 1000

COPY locustfile.py /mnt/locust/locustfile.py
COPY custom_locust_config.conf /mnt/locust/custom_locust_config.conf

WORKDIR /mnt/locust

ENTRYPOINT ["locust", "--config", "custom_locust_config.conf"]
CMD ["--host", "localhost"]
