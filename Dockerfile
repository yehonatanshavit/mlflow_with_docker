# import python
FROM public.ecr.aws/lambda/python:3.8

# run requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# run example
COPY main.py ./
CMD ["main.lambda_handler"]