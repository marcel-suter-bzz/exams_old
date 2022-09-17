import uuid

from flask import make_response
from flask_restful import Resource, fields, reqparse

from data.PersonDAO import PersonDAO
from model.Person import Person
from util.authorization import token_required, teacher_required
from data.ExamDAO import ExamDAO
from model.Exam import Exam

class ExamService(Resource):
    """
    services for CRUD of a single exam

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('exam_uuid', location='form', help='uuid')
        self.parser.add_argument('event_uuid', location='form', help='event_uuid')
        self.parser.add_argument('student', location='form', help='student')
        self.parser.add_argument('teacher', location='form', help='teacher')
        self.parser.add_argument('cohort', location='form', help='cohort')
        self.parser.add_argument('module', location='form', help='module')
        self.parser.add_argument('exam_num', location='form', help='exam-num')
        self.parser.add_argument('duration', location='form', type=str, help='Muss eine Ganzzahl sein')
        self.parser.add_argument('missed', location='form', help='Muss ein gültiges Datum sein')
        self.parser.add_argument('remarks', location='form', help='remarks')
        self.parser.add_argument('tools', location='form', help='tools')

        self.parser.add_argument('status', location='form', help='status')

    def get(self, exam_uuid):
        """
        gets an exam identified by the uuid
        :param exam_uuid: the unique key
        :return: http response
        """
        exam_dao = ExamDAO()
        exam = exam_dao.read_exam(exam_uuid)
        data = '{}'
        http_status = 404
        if exam is not None:
            http_status = 200
            data = exam.to_json()

        return make_response(
            data, http_status
        )

    @teacher_required
    def post(self):
        """
        creates a new exam
        :return: http response
        """
        args = self.parser.parse_args()
        self.save(args)
        return make_response('exam saved', 201)

    @teacher_required
    def put(self):
        """
        updates an existing exam identified by the uuid
        :return:
        """
        args = self.parser.parse_args()
        self.save(args)
        return make_response('exam saved', 200)

    def save(self,args):
        """
        saves the new or updated exam
        :param args:
        :return:
        """
        if args.exam_uuid is None or args.exam_uuid == '':
            args.exam_uuid = str(uuid.uuid4())
        person_dao = PersonDAO()
        teacher = person_dao.read_person(args.teacher)
        student = person_dao.read_person(args.student)
        exam = Exam(
            exams_uuid=args.exam_uuid,
            teacher=teacher,
            student=student,
            cohort=args.cohort,
            module=args.module,
            exam_num=args.exam_num,
            duration=args.duration,
            missed=args.missed,
            remarks=args.remarks,
            tools=args.tools,
            event_uuid=args.event_uuid,
            status=args.status
        )
        exam_dao = ExamDAO()
        exam_dao.save_exam(exam)

if __name__ == '__main__':
    ''' Check if started directly '''
    pass
