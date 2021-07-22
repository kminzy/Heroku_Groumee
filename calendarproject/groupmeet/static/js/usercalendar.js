$(document).ready(function(){ 
    $(".date").click(function () {                     // 어떤 날짜를 누르면 이하 내용들을 실행
                                                             /* ★★★실행시키고자 하는 것★★★
                                                                : 특정 날짜를 누르면 그 날짜에 테두리가 생기고
                                                                  사이드바가 나오는데, 그 바에는 그 날에 해당
                                                                  하는 일정들과 일정들의 개수, 클릭한 날짜, 새
                                                                  일정 생성 버튼이 있다.  */ 
      $(".date").css("border", "0");                   // 다른 날짜들에 있는 테두리를 없애고
      $(this).css("border", "4px solid #1f33e2")       // 클릭한 날짜에 테두리가 생긴다. 

      let day = $(this).html().split('<')[0];          // 클릭한 날짜의 날(ex : 15, 17, 31...)을 가져와서
      $("#cur_day").text(day);                         // 사이드바의 날짜로 한다. 즉 클릭한 날짜가 사이드바에 표시되게 됨

      let param = {                                    // 클릭한 날짜의 년/월/일을 객체형태로. 얘를 ajax통신에 사용할 것임
        'year' : cur_year,
        'month' : cur_month,
        'day' : day
      }

      $.ajax({                                         // ajax 통신
        url : show_userschedule_url,                   // 통신할 url. urlspy에서 이 url에 매칭되는 views가 실행됨
        type : 'POST',                                 // 어떤 방식으로 통신할 것인지. GET or POST
        headers : {
          'X-CSRFTOKEN' : csrf_token
        },
        data : JSON.stringify(param),                  // 보낼 데이타. 객체 param을 json형태로 바꿔줬음
        success:function(data){                        // 통신에 성공하면 이하 내용 실행. 파라미터 data는 view에서 넘겨받은 것임

          let schedules_list = JSON.parse(data);                            // view에서 받은 json형태의 데이터를 js객체형태로 바꿔서 할당
                                                                            // 즉 schedules_list는 js객체들의 리스트형태
                                                                            // ex) [json_data_01, json_data_02, json_data_03, ...]
                                                                            // shcedules_list는 클릭한 날짜의 일정들의 리스트임
          $("#num-of-schedules").text(schedules_list.length); // 사이드바에서 'N개의 일정들이 있습니다'라는 문장에서 N을 표기
          $(".content-section").empty();                      // 일정들이 채워질 영역을 비움 -> 7일날 일정 보다가 8일 일정 볼때, 7일 일정
                                                              // 은 날리고 8일 일정만 봐야 하므로 

          if (!schedules_list.length){
            $(".content-section").append(                                    // 사이드바에 일정 추가
              '<div class="is-not-schedule">\
                <i class="fas fa-calendar-times"></i>\
                <p>아무 일정도 없습니다.<br>새 일정을 추가해보세요!</p>\
              </div>'
            );
          }
          else{                                                 // schedules_list의 사이즈가 0아 이니라면 
            for(let i=0; i<schedules_list.length; i++){         // 각 일정들을 실실적으로 사이드바에 추가할 것임
            let start_time = schedules_list[i]['fields']['start'].split('T');
            start_time = start_time[0] + ' ' + start_time[1].slice(0, 5);   // start_time : 그 일정의 시작 시간 ex) 2021-07-16 19:00

            let end_time = schedules_list[i]['fields']['end'].split('T');
            end_time = end_time[0] + ' ' + end_time[1].slice(0, 5);         // end_time : 그 일정의 종료 시간 ex) 2021-07-16 21:30

            let time = start_time + ' ~ ' + end_time;                       
            let content = schedules_list[i]['fields']['title'].slice(0, 20);  // content : 그 일정의 내용, 단 20글자만 가져옴

            $(".content-section").append(                                    // 사이드바에 일정 추가
              '<div class="content">\
                <div class="top">\
                  <div>' + time + '</div><i class="fas fa-trash-alt delete-schedule" onclick="delete_schedule(this, ' + schedules_list[i]['pk'] + ');"></i>\
                </div>\
                <div class="mid">' 
                  + content
                + '</div>\
              </div>'
            );
          }
          }
        },
        error:function(){                              // 통신에 실패하면 이하 내용 실행
          alert("데이터를 가져오는데 실패했습니다");
        }
      });                                             // ajax 통신 종료

      $("#Sidebar").css("right", "0");                 // 사이드바 나오게 하기
    });

    $(".go-add-userschedule").click(function (){
      // let form_field_month = (cur_month < 10) ? ("0" + cur_month) : cur_month;
      // let form_field_day = (day < 10) ? ("0" + day) : day;
      // 폼 필드 중 start, end의 기본값을 세팅할 것임. 클릭한 날짜를 기준.
      let form_field_month = cur_month.padStart(2, '0');            // month가 10보다 작으면 앞에 0을 붙임 ex) 7 -> 07
      let form_field_day = $("#cur_day").text().padStart(2, '0');   // day가 10보다 작으면 앞에 0을 붙임 ex) 7 -> 07
                                                                    // type이 datetime-local인 input태그의 value수정 시 이렇게 0이 붙은 값들을 써야 해서
      $('#id_start').val(cur_year + '-' + form_field_month + '-' + form_field_day + 'T00:00');
      $('#id_end').val(cur_year + '-' + form_field_month + '-' + form_field_day + 'T00:00');
      $('#id_title').val('');

      $('.modal-body #add-userschedule_form ul').empty();
    });
    
    $(".add-userschedule").click(function () {
      const start_time = document.getElementById("id_start").value;
      const end_time = document.getElementById("id_end").value;
      const title = document.getElementById("id_title").value;
      const csrf = document.getElementsByName('csrfmiddlewaretoken');

      const fd = new FormData();

      fd.append('csrfmiddlewaretoken', csrf[0].value);
      fd.append('start', start_time);
      fd.append('end', end_time);
      fd.append('title', title);
      
      $.ajax({
        url : create_userschedule_url,
        type : 'POST',
        headers : {
          'X-CSRFTOKEN' : csrf_token
        },
        data : fd,
        success:function(data){

          if(data['result'] === "success"){                   // 작성한 폼이 유효했다면 redirect
            setTimeout(function() {
              location.href = "";
            }, 300);
          }
          else{                                               // 작성한 폼이 유효 X -> 에러메시지 출력
            form_errors = JSON.parse(data['form_errors'])
            
            $('#add-userschedule_form ul').empty();
           
            $.each(form_errors, function(i, value){
              $.each(value, function(j, message){
                let error_message = '<li>' + value[j]['message'] + '</li>';
                $("ul[id*='" + i +"']").append(error_message);
              });
            });
          }

        },
        error:function(){
          alert("일정을 생성하는데 실패했습니다");
        },
        cache : false,
        contentType: false,
        processData: false

      });

    });
  });

  function delete_schedule(self, pk) {
    let result = confirm("정말 이 일정을 삭제하시겠습니까?");
    if (result){

      let param = {
        'pk' : pk
      }

      $.ajax({
        url : delete_userschedule_url,
        type : 'POST',
        headers : {
          'X-CSRFTOKEN' : csrf_token
        },
        data : JSON.stringify(param),
        success:function(data){
          setTimeout(function() {
            location.href = "";
          }, 300);
          // $(self).parent().parent().remove();

        },
        error:function(){
          alert("일정을 삭제하는데 실패했습니다");
        }
      });
    }
    else{
      ;
    }
  }

  function closeSidebar() {                                           // 사이드바 닫기
    document.getElementById("Sidebar").style.right = "-25vw";
  }

  function go_prev_month() {                                          // 이전 달로 가기
    if (document.getElementById("Sidebar").style.right === "0px"){    // 사이드바가 보이는 상태면, 사이드바를 먼저 닫고 저번달 보여줌
      closeSidebar();
      setTimeout(function() {
        location.href = userCalendar_view_url + "?" + prev_month;
      }, 400);
    }
    else{                                                            // 사이드바가 닫힌 상태면, 바로 저번달 보여줌
      location.href = userCalendar_view_url + "?" + prev_month;
    }
  }

  function go_next_month() {                                          // 다음 달로 가기
    if (document.getElementById("Sidebar").style.right === "0px"){    // 사이드바가 보이는 상태면, 사이드바를 먼저 닫고 다음달 보여줌
      closeSidebar();
      setTimeout(function() {
        location.href = userCalendar_view_url + "?" + next_month;
      }, 400);
    }
    else{                                                            // 사이드바가 닫힌 상태면, 바로 다음달 보여줌
      location.href = userCalendar_view_url + "?" + next_month;
    }
  }