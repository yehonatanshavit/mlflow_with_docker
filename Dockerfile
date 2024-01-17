# import python
FROM public.ecr.aws/lambda/python:3.8

# run requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# run example
COPY full_code.py ./
CMD ["full_code.lambda_handler"]