var currentPage = passedPage + 1;
var totalPageNum = 12 


function goNextPage() {
    if (currentPage <= totalPageNum) {
        opener.PageMove2019AfterVersion(currentPage);
        console.log(`${currentPage} 페이지를 수강완료했습니다.`);
        currentPage += 1;

        setTimeout(function() {
            goNextPage();
        }, 1000);
    } else {
        alert('강의 수강이 완료되었습니다!');
    }
}

function runKmuMacro() {
    console.log(`현재 ${currentPage} 페이지를 수강중입니다.`);
    setTimeout(function () {
        goNextPage();
    }, 1000)
}

runKmuMacro();
