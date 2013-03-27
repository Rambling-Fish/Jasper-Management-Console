#!/bin/bash

set -e

JTADIR=/opt/jasper/jasper-1.1
ACTION=$1
PARAM1=$2
PARAM2=$3

J_PID=""
M_PID=""
UNAME=`uname`
OS="$UNAME"
USER="jasper"

# Setting JTA's Status Values
NOT_FOUND="0"
NAME_REQUIRED="1"
TRANSITION="2"
UNDEPLOYED="3"
DEPLOYED="4"
# Initial Status
JTA_STATUS="$NOT_FOUND"


# PIDs

function get_j_pid {
    J_PID=""
    J_PID=`ps ax | grep java | grep JECore | cut -d' ' -f1`
    if [ -z "$J_PID" ]
    then
J_PID=`ps ax | grep java | grep JECore | cut -d' ' -f2`
      if [ -z "$J_PID" ]
      then
J_PID=`ps ax | grep java | grep JECore | cut -d' ' -f3`
      fi
fi
}

function get_m_pid {
    M_PID=""
    M_PID=`ps ax | grep mule | grep wrapper.pidfile | cut -d' ' -f1`
    if [ -z "$M_PID" ]
    then
M_PID=`ps ax | grep mule | grep wrapper.pidfile | cut -d' ' -f2`
      if [ -z "$M_PID" ]
      then
M_PID=`ps ax | grep mule | grep wrapper.pidfile | cut -d' ' -f3`
      fi
fi
}

# STATUS

function status_j {
   get_j_pid
   if [ -z "$J_PID" ]; then
echo "0"
   else
echo "1"
   fi
}

function status_m {
   get_m_pid
   if [ -z "$M_PID" ]; then
echo "0"
   else
echo "1"
   fi
}

# STOP
function stop_j {
   get_j_pid
   if [ -z "$J_PID" ]; then
      echo "JSB is not running." 
   else
      echo -n "Stopping JSB.."
      cd $JTADIR/jsb-core/bin
      ./jsb stop 
      if [ "$OS" == 'Linux' ]; then
         rm /opt/jasper/jasper-1.1/jsbAutoStart
      fi
      echo ".. Done."
   fi
}

function stop_m {
   get_m_pid
   if [ -z "$M_PID" ]; then
      echo "JTA Server is not running." 
   else
      echo -n "Stopping JTA Server.."
      cd $JTADIR/jsb-core/mule-standalone-3.3.0/bin
      ./mule stop
      if [ "$OS" == 'Linux' ]; then
         rm $JTADIR/jtaAutoStart
      fi 
      echo ".. Done."
   fi
}

# KILL
function force_stop_j {
   get_j_pid
   if [ -z "$J_PID" ]; then
      echo "JSB is not running." 
   else
      echo -n "Forcing JSB Server to Stop.."
      kill $J_PID 
      if [ "$OS" == 'Linux' ]; then
         rm $JTADIR/jsbAutoStart
      fi
      echo ".. Done."
   fi
}

function force_stop_m {
   get_m_pid
   if [ -z "$M_PID" ]; then
      echo "JTA Server is not running." 
   else
      echo -n "Forcing JTA Server to Stop.."
      kill $M_PID
      if [ "$OS" == 'Linux' ]; then
         rm $JTADIR/jtaAutoStart
      fi 
      echo ".. Done."
   fi
}

# AUTODISCOVERY
function auto_d {
    cd $JTADIR
    cd ../jmp
    su "$USER" -c "./jmp_main.py"
}

# START
function start_j {
  get_j_pid
  if [ -z "$J_PID" ]; then
      echo  "Starting JSB.. jasper.management.sh"
      cd $JTADIR/jsb-core/bin
      su "$USER" -c "./jsb start" 
      if [ "$OS" == 'Linux' ]; then
         if [ ! -L $JTADIR/jsbAutoStart ]; then
            su "$USER" -c "ln -s $JTADIR/jsb-core/jsbAutoStart $JTADIR/jsbAutoStart"
         fi
      fi
  else
      echo "JSB is already running, PID=$J_PID"
  fi
}

function start_m {
   get_m_pid
   if [ -z "$M_PID" ]; then
      echo  "Starting JTA Server.."
      cd $JTADIR/jsb-core/mule-standalone-3.3.0/bin
      su "$USER" -c "./mule start"
      cd ../../../ 
      if [ "$OS" == 'Linux' ]; then
         if [ ! -L $JTADIR/jtaAutoStart ]; then
            su "$USER" -c "ln -s $JTADIR/jsb-core/jtaAutoStart $JTADIR/jtaAutoStart"
         fi
      fi     
   else
      echo "JTA Server is already running, PID=$M_PID"
   fi
}

function start {
    start_j
    start_m
    exit 1
}

function stop {
    stop_m
    stop_j
    exit 1
}

function force_stop {
    force_stop_m
    force_stop_j
    exit 1
}

# MAIN CASE

case ${ACTION} in
# key: jasper.management[undeployed]
undeployed)
 cd $JTADIR/JTAs
 for file in *
    do
       if [ -x "$file" ]; then
          echo "$file"
       fi
    done 
 cd ..
;;   
# key: jasper.management[deployed] 
discovery)
    auto_d
;;
deployed)   
    cd $JTADIR/jsb-core/mule-standalone-3.3.0/apps/
    JTAList=`find . -maxdepth 1 -name "*-anchor.txt" | grep -v default-anchor.txt | rev | cut -c 12- | rev | cut -c 3-`
    if [ -z "$JTAList" ]; then
       echo "None"
    else
       echo "$JTAList"
    fi   
;;
# key: jasper.management[jsbserver]     
jsbserver)
    status_j
;;
# key: jasper.management[jtaserver]    
jtaserver)
    status_m
;;
# key: jasper.management[jtastatus,jtaName]    
jtastatus)
    if [ -z ${PARAM1} ]; then
       # JTA Name required
       JTA_STATUS="$NAME_REQUIRED"
       echo "$JTA_STATUS" 
    else
      cd $JTADIR/JTAs
      # Undeployed
      if [ -d "${PARAM1}" ] || [ -a "${PARAM1}.zip" ]; then JTA_STATUS="$UNDEPLOYED"
      else 
        cd $JTADIR/jsb-core/mule-standalone-3.3.0/apps/
        # Deployed
        if [ -d "${PARAM1}" ] && [ -a "${PARAM1}-anchor.txt" ]; then 
          JTA_STATUS="$DEPLOYED"
        else
          if [ -d "${PARAM1}" ] || [ -a "${PARAM1}-anchor.txt" ]; then
            # Unestable or transition 
            JTA_STATUS="$TRANSITION"
          fi
        fi
      fi

      echo "$JTA_STATUS"
         
    fi
;;
start)
    case "${PARAM1}" in
    jsb)
      start_j
    ;;
    jta)
      start_m
    ;;
    *)
      start
    ;;
    esac
;;            
stop)
    case "${PARAM1}" in
    jsb)
        stop_j
    ;;
    jta)
        stop_m
    ;;
    *)
        stop
    ;;
    esac
;;
kill)
    case "${PARAM1}" in
    jsb)
        force_stop_j
    ;;
    jta)
        force_stop_m
    ;;
    *)
        force_stop
    ;;
    esac
;;
*)   
   /bin/echo ZBX_NOTSUPPORTED   
;; 
esac

