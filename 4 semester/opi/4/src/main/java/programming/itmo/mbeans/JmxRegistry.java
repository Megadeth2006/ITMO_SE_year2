package programming.itmo.mbeans;

import java.lang.management.ManagementFactory;
import java.util.logging.Logger;
import javax.management.MBeanServer;
import javax.management.ObjectName;

public final class JmxRegistry {
    private static final Logger LOGGER = Logger.getLogger(JmxRegistry.class.getName());
    private static final String POINT_STATISTICS_OBJECT_NAME = "programming.itmo:type=PointStatistics";
    private static final String CLICK_INTERVAL_OBJECT_NAME = "programming.itmo:type=ClickInterval";

    private static final PointStatistics POINT_STATISTICS = new PointStatistics();
    private static final ClickInterval CLICK_INTERVAL = new ClickInterval();

    private JmxRegistry() {
    }

    public static synchronized void registerMBeans() {
        try {
            LOGGER.info("Registering monitoring MBeans");
            MBeanServer mBeanServer = ManagementFactory.getPlatformMBeanServer();
            registerIfNeeded(mBeanServer, new ObjectName(POINT_STATISTICS_OBJECT_NAME), POINT_STATISTICS);
            registerIfNeeded(mBeanServer, new ObjectName(CLICK_INTERVAL_OBJECT_NAME), CLICK_INTERVAL);
            LOGGER.info("Monitoring MBeans registration completed");
        } catch (Exception e) {
            throw new IllegalStateException("Cannot register monitoring MBeans", e);
        }
    }

    public static synchronized void unregisterMBeans() {
        try {
            LOGGER.info("Unregistering monitoring MBeans");
            MBeanServer mBeanServer = ManagementFactory.getPlatformMBeanServer();
            unregisterIfNeeded(mBeanServer, new ObjectName(POINT_STATISTICS_OBJECT_NAME));
            unregisterIfNeeded(mBeanServer, new ObjectName(CLICK_INTERVAL_OBJECT_NAME));
            LOGGER.info("Monitoring MBeans unregistration completed");
        } catch (Exception e) {
            throw new IllegalStateException("Cannot unregister monitoring MBeans", e);
        }
    }

    public static PointStatistics getPointStatistics() {
        return POINT_STATISTICS;
    }

    public static ClickInterval getClickInterval() {
        return CLICK_INTERVAL;
    }

    private static void registerIfNeeded(MBeanServer mBeanServer, ObjectName objectName, Object mBean)
            throws Exception {
        if (!mBeanServer.isRegistered(objectName)) {
            mBeanServer.registerMBean(mBean, objectName);
            LOGGER.info("Registered MBean " + objectName);
        } else {
            LOGGER.info("MBean already registered " + objectName);
        }
    }

    private static void unregisterIfNeeded(MBeanServer mBeanServer, ObjectName objectName) throws Exception {
        if (mBeanServer.isRegistered(objectName)) {
            mBeanServer.unregisterMBean(objectName);
            LOGGER.info("Unregistered MBean " + objectName);
        } else {
            LOGGER.info("MBean was not registered " + objectName);
        }
    }
}
