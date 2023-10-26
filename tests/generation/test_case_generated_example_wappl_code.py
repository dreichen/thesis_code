# it is necessary to not only test the generation but also the code that comes from the generation
# a first step is to use the following code to ensure there are no exceptions thrown whenever the example.wappl code that results in the generated code is executed
if __name__ == '__main__':
    hw = HomeworkEntity({"text": "hi", "test": 5, "grade": 5.0})
    assignment = AssignmentEntity({"title" : "lawestrase", "homework": hw})
    task = HomeworkGradingTask(hw)
    task.step_gradeAssignment(assignment, {"grade": Grade(5)})